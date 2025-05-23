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
                ci.id, ci.quantity, ci.price, 
                p.id, p.name, p.description, p.image, ca.id, ca.name
            FROM carts c
            LEFT JOIN cart_items ci ON c.id = ci.cart_id
            LEFT JOIN products p ON ci.product_id = p.id
            LEFT JOIN categories ca ON p.category_id = ca.id
            WHERE c.user_id = %s AND c.status = 'active'
            """, (user_id,))
            rows = cur.fetchall()
            cur.close()

            if rows is None:
                raise Exception("Cart not found")

            if len(rows) == 0:
                return Cart()

            cart = Cart(id=rows[0][0], user_id=rows[0][1], status=rows[0][2], cart_items=[])

            # if cart is empty
            if rows[0][3] is None:
                return cart

            cart.cart_items = [
                CartItem(
                    id=row[3],
                    quantity=row[4],
                    price=row[5],
                    product=Product(
                        id=row[6],
                        name=row[7],
                        description=row[8],
                        image=row[9],
                        category=Category(
                            id=row[10],
                            name=row[11]
                        )
                    ),
                )
                for row in rows
            ]
            return cart
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_cart_by_id(self, cart_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT 
                c.id, c.user_id, c.status,
                ci.id, ci.quantity, ci.price, 
                p.id, p.name, p.description,
                p.image, ca.id, ca.name
            FROM carts c
            LEFT JOIN cart_items ci ON c.id = ci.cart_id
            LEFT JOIN products p ON ci.product_id = p.id
            LEFT JOIN categories ca ON p.category_id = ca.id
            WHERE c.id = %s
            """, (cart_id,))
            rows = cur.fetchall()
            cur.close()

            if rows is None:
                raise Exception("Cart items not found")

            cart = Cart(id=rows[0][0], user_id=rows[0][1], status=rows[0][2], cart_items=[])

            # if cart is empty
            if rows[0][3] is None:
                return cart

            cart.cart_items = [
                CartItem(
                    id=row[3],
                    quantity=row[4],
                    price=row[5],
                    product=Product(
                        id=row[6],
                        name=row[7],
                        description=row[8],
                        image=row[9],
                        category=Category(
                            id=row[10],
                            name=row[11]
                        )
                    ),
                )
                for row in rows if row is not None
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

            return row[0] if row[0] is not None else 0
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

            return row[0] if row[0] is not None else 0
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

    def get_cart_item_by_product_id(self, cart_id: int, product_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            row = cur.fetchone()
            cur.close()
            if row is None:
                return None
            return CartItem(id=row[0], cart_id=row[1], product=Product(id=row[2]), quantity=row[3], price=row[4])
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def add_to_cart(self, cart_id: int, product_id: int, quantity: int = 1):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cur.fetchone()
            if price is None:
                raise Exception("Product not found")

            cur.execute("INSERT INTO cart_items (cart_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (cart_id, product_id, quantity, price))
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
        