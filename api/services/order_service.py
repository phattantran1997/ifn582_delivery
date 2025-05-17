from api.services.base_service import BaseService
from api.models.shipping_method import ShippingMethod
from api.models.order import Order
from api.models.order_item import OrderItem

class OrderService(BaseService):
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
    