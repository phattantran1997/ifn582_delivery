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
            return [Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    def get_all_shipping_methods(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM shipping_methods ORDER BY id")
            rows = cur.fetchall()
            cur.close()
            return [ShippingMethod(row[0], row[1], row[2], row[3]) for row in rows]
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
            """, (user_id, cart_id, shipment_id, 'pending', total_amount))
            order_id = cur.lastrowid

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
                    id=row[0],
                    user_id=row[1],
                    cart_id=row[2],
                    status=row[3],
                    total_amount=float(row[4]),
                    created_at=row[5],
                    shipment=Shipment(
                        recipient_name=row[6],
                        address=row[7],
                        phone=row[8],
                        shipment_method=ShippingMethod(
                            id=row[9],
                            name=row[10]
                        )
                    ),
                    items=[]
                )
                
                # Get items for each order
                cur.execute("""
                    SELECT 
                        oi.id, oi.order_id, oi.product_id, oi.quantity, oi.price,
                        p.id, p.name, p.description, p.image
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """, (order.id,))
                
                for item_row in cur.fetchall():
                    item = OrderItem(
                        id=item_row[0],
                        order_id=item_row[1],
                        product_id=item_row[2],
                        quantity=item_row[3],
                        price=float(item_row[4]),
                        product=Product(
                            id=item_row[5],
                            name=item_row[6],
                            description=item_row[7],
                            image=item_row[8]
                        )
                    )
                    order.items.append(item)
                
                orders.append(order)
            
            cur.close()
            return orders
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    