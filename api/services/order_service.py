from api.services.base_service import BaseService
from api.models.shipping_method import ShippingMethod
from api.models.order import Order
from api.models.shipment import Shipment
from api.models.product import Product
from api.models.shipping_method import ShippingMethod
from api.models.order_item import OrderItem

class OrderService(BaseService):
    def get_all_orders(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM orders ORDER BY id")
            rows = cur.fetchall()
            cur.close()
            return [Order(
                id=row['id'],
                user_id=row['user_id'],
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
            if user_id:
                cur.execute("""
                SELECT 
                    o.id, o.user_id, o.cart_id, o.status, o.total_amount, o.created_at,
                    s.recipient_name, s.address, s.phone, sm.id as delivery_method_id, sm.name as delivery_method_name
                FROM orders o
                JOIN shipments s ON o.shipment_id = s.id
                JOIN shipping_methods sm ON s.shipping_method_id = sm.id
                WHERE o.user_id = %s
                ORDER BY o.created_at DESC
            """, (user_id,))
            else:
                cur.execute("""
                SELECT 
                    o.id, o.user_id, o.cart_id, o.status, o.total_amount, o.created_at,
                    s.recipient_name, s.address, s.phone, sm.id as delivery_method_id, sm.name as delivery_method_name
                FROM orders o
                JOIN shipments s ON o.shipment_id = s.id
                JOIN shipping_methods sm ON s.shipping_method_id = sm.id
                ORDER BY o.created_at DESC
            """)
            orders = []
            for row in cur.fetchall():
                order = Order(
                    id=row['id'],
                    user_id=row['user_id'],
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
                )
                
                # Get items for each order
                cur.execute("""
                    SELECT 
                        oi.id, oi.order_id, oi.product_id, oi.quantity, oi.price,
                        p.id product_id, p.name product_name, p.description product_description, p.image product_image
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """, (order.id,))
                
                for row in cur.fetchall():
                    item = OrderItem(
                        id=row['id'],
                        order_id=row['order_id'],
                        product_id=row['product_id'],
                        quantity=row['quantity'],
                        price=row['price'],
                        product=Product(
                            id=row['product_id'],
                            name=row['product_name'],
                            description=row['product_description'],
                            image=row['product_image']
                        )
                    )
                    order.items.append(item)
                
                orders.append(order)
            
            cur.close()
            return orders
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    