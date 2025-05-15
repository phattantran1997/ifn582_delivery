from api.services.base_service import BaseService
from api.models.cart import Cart
from api.models.cart_items import CartItem
from api.models.product import Product
from api.models.category import Category

class CartService(BaseService):
    def get_cart_by_user_id(self, user_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT 
                c.id, c.user_id, c.status, 
                ci.product_id, ci.quantity, ci.price, 
                p.id, p.name, ca.id, ca.name
            FROM carts c
            JOIN cart_items ci ON c.id = ci.cart_id
            JOIN products p ON ci.product_id = p.id
            JOIN categories ca ON p.category_id = ca.id
            WHERE c.user_id = %s AND c.status = 'active'
            """, (user_id,))
            rows = cur.fetchall()
            cur.close()

            if rows is None:
                raise Exception("Cart not found")

            cart = Cart(id=rows[0][0], user_id=rows[0][1], status=rows[0][2], cart_items=[])

            cart.cart_items = [
                CartItem(
                    id=row[3],
                    quantity=row[4],
                    price=row[5],
                    product=Product(
                        id=row[6],
                        name=row[7],
                        category=Category(
                            id=row[8],
                            name=row[9]
                        )
                    ),
                )
                for row in rows
            ]
            return cart
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    # get cart subtotal includes GST

    def get_cart_by_id(self, cart_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT 
                ci.id, ci.quantity, ci.price, 
                p.id, p.name, ca.id, ca.name
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            JOIN categories ca ON p.category_id = ca.id
            WHERE ci.cart_id = %s
            """, (cart_id,))
            rows = cur.fetchall()
            cur.close()

            if rows is None:
                raise Exception("Cart items not found")

            cart = Cart(id=rows[0][0], user_id=rows[0][1], status=rows[0][2], cart_items=[])

            cart.cart_items = [
                CartItem(
                    id=row[0],
                    quantity=row[1],
                    price=row[2],
                    product=Product(
                        id=row[3],
                        name=row[4],
                        category=Category(
                            id=row[5],
                            name=row[6]
                        )
                    ),
                )
                for row in rows
            ]
            return cart
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_cart_subtotal(self, cart_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT SUM(ci.quantity * ci.price) AS subtotal
            FROM cart_items ci
            WHERE ci.cart_id = %s
            """, (cart_id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Cart not found")

            return row[0]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_cart_item_quantity(self, cart_item_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT quantity
            FROM cart_items
            WHERE id = %s
            """, (cart_item_id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Cart item not found")

            return row[0]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def update_cart_item_quantity(self, cart_item_id: int, quantity: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
                UPDATE cart_items
                SET quantity = quantity + %s
                WHERE id = %s
            """, (quantity, cart_item_id))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def delete_cart_item(self, cart_item_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            DELETE FROM cart_items
            WHERE id = %s
            """, (cart_item_id,))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        