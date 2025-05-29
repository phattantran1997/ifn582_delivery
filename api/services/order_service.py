from api.services.base_service import BaseService
from api.models.shipping_method import ShippingMethod
from api.models.order import Order
from api.models.shipment import Shipment
from api.models.product import Product
from api.models.user import User
from api.models.order_item import OrderItem

class OrderService(BaseService):
    def get_all_orders(self):
        try:
            cur = self.get_cursor()
            cur.execute("""
                SELECT 
                    orders.id,
                    orders.user_id,
                    users.username,
                    orders.cart_id,
                    orders.status,
                    orders.total_amount,
                    orders.created_at,
                    shipments.recipient_name,
                    shipments.address,
                    shipments.phone,
                    shipping_methods.id as delivery_method_id,
                    shipping_methods.name as delivery_method_name
                FROM orders
                JOIN users ON orders.user_id = users.id
                JOIN shipments ON orders.shipment_id = shipments.id
                JOIN shipping_methods ON shipments.shipping_method_id = shipping_methods.id
                ORDER BY orders.id
            """)
            rows = cur.fetchall()
            cur.close()
            return [Order(
                id=row['id'],
                user=User(
                    id=row['user_id'],
                    username=row['username'],
                ),
                cart_id=row['cart_id'],
                status=row['status'],
                total_amount=row['total_amount'],
                created_at=row['created_at'],
                shipment=Shipment(
                    recipient_name=row['recipient_name'],
                    address=row['address'],
                    phone=row['phone'],
                    shipment_method=ShippingMethod(
                        id=row['delivery_method_id'],
                        name=row['delivery_method_name']
                    )
                ),
                items=[]
            ) for row in rows]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_all_shipping_methods(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM shipping_methods ORDER BY id")
            rows = cur.fetchall()
            cur.close()
            return [ShippingMethod(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                fee=row['fee']
            ) for row in rows]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")


    def create_order(
        self,
        recipient_name,
        phone,
        address,
        delivery_method_id,
        user_id,
        cart_id,
        total_amount
    ):
        try:
            cur = self.get_cursor()
            cur.execute("""
            INSERT INTO shipments (shipping_method_id, recipient_name, address, phone)
            VALUES (%s, %s, %s, %s)
            """, (delivery_method_id, recipient_name, address, phone))
            shipment_id = cur.lastrowid

            cur.execute("""
            INSERT INTO orders (user_id, cart_id, shipment_id, status, total_amount)
            VALUES (%s, %s, %s, %s, %s)
            """, (user_id, cart_id, shipment_id, 'delivered', total_amount))
            order_id = cur.lastrowid

            cur.execute("UPDATE carts SET status = 'abandoned' WHERE id = %s", (cart_id,))

            # update product quantity in products table based on cart items quantity
            cur.execute("""
            UPDATE products p
            JOIN cart_items ci ON p.id = ci.product_id
            SET p.quantity = p.quantity - ci.quantity
            WHERE ci.cart_id = %s
            """, (cart_id,))

            cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            SELECT %s, product_id, quantity, price
            FROM cart_items
            WHERE cart_id = %s
            """, (order_id, cart_id))
            self.mysql.connection.commit()
            cur.close()
            return order_id
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_orders_by_user_id(self, user_id=None):
        try:
            cur = self.get_cursor()
            # Determine the base query based on whether a user_id is provided
            base_query = """
                SELECT 
                    orders.id, 
                    orders.user_id,
                    users.username,
                    orders.cart_id, 
                    orders.status, 
                    orders.total_amount, 
                    orders.created_at,
                    shipments.recipient_name, 
                    shipments.address, 
                    shipments.phone, 
                    shipping_methods.id as delivery_method_id, 
                    shipping_methods.name as delivery_method_name
                FROM orders
                JOIN users ON orders.user_id = users.id
                JOIN shipments ON orders.shipment_id = shipments.id
                JOIN shipping_methods ON shipments.shipping_method_id = shipping_methods.id
            """
            if user_id:
                cur.execute(base_query + " WHERE orders.user_id = %s ORDER BY orders.created_at DESC", (user_id,))
            else:
                cur.execute(base_query + " ORDER BY orders.created_at DESC")

            orders_data = cur.fetchall()
            orders = []

            for order_row in orders_data:
                order = Order(
                    id=order_row['id'],
                    user=User(
                        id=order_row['user_id'],
                        username=order_row['username'],
                    ),
                    cart_id=order_row['cart_id'],
                    status=order_row['status'],
                    total_amount=order_row['total_amount'],
                    created_at=order_row['created_at'],
                    shipment=Shipment(
                        recipient_name=order_row['recipient_name'],
                        address=order_row['address'],
                        phone=order_row['phone'],
                        shipment_method=ShippingMethod(
                            id=order_row['delivery_method_id'],
                            name=order_row['delivery_method_name']
                        )
                    ),
                    items=[]
                )
                
                # Get items for each order
                cur.execute("""
                    SELECT 
                        oi.id, oi.order_id, oi.product_id, oi.quantity, oi.price,
                        p.name AS product_name, p.description AS product_description, 
                        p.image AS product_image, p.quantity AS product_current_quantity  
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """, (order.id,))
                
                order_items_data = cur.fetchall()
                for item_row in order_items_data:
                    item = OrderItem(
                        id=item_row['id'],
                        order_id=item_row['order_id'],
                        product_id=item_row['product_id'],
                        quantity=item_row['quantity'], 
                        price=item_row['price'],
                        product=Product(
                            id=item_row['product_id'],
                            name=item_row['product_name'],
                            description=item_row['product_description'],
                            image=item_row['product_image'],
                            quantity=item_row['product_current_quantity']  
                        )
                    )
                    order.items.append(item)
                
                orders.append(order)
            
            return orders
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if cur:
                cur.close()