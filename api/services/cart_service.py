from api.services.base_service import BaseService
from api.models.cart import Cart
from api.models.cart_items import CartItem
from api.models.product import Product
from api.models.category import Category

class CartService(BaseService):
    def create_cart(self, user_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("INSERT INTO carts (user_id, status) VALUES (%s, 'active')", (user_id,))
            self.mysql.connection.commit()
            cur.close()
            return Cart(id=cur.lastrowid, user_id=user_id, status='active', cart_items=[])
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_cart_by_user_id(self, user_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
            SELECT 
                carts.id,
                carts.user_id,
                carts.status,
                cart_items.id cart_item_id,
                cart_items.quantity,
                cart_items.price,
                products.id product_id,
                products.name product_name,
                products.description product_description,
                products.image product_image,
                products.quantity AS product_quantity,
                categories.id category_id,
                categories.name category_name
            FROM carts
            LEFT JOIN cart_items ON carts.id = cart_items.cart_id
            LEFT JOIN products ON cart_items.product_id = products.id
            LEFT JOIN categories ON products.category_id = categories.id
            WHERE carts.user_id = %s AND carts.status = 'active'
            """, (user_id,))
            rows = cur.fetchall()
            cur.close()

            if rows is None:
                raise Exception("Cart not found")

            if len(rows) == 0:
                return None

            cart = Cart(id=rows[0]['id'], user_id=rows[0]['user_id'], status=rows[0]['status'], cart_items=[])

            # if cart is empty
            if rows[0]['cart_item_id'] is None:
                return cart

            cart.cart_items = [
                CartItem(
                    id=row['cart_item_id'],
                    quantity=row['quantity'],
                    price=row['price'],
                    product=Product(
                        id=row['product_id'],
                        name=row['product_name'],
                        description=row['product_description'],
                        image=row['product_image'],
                        quantity=row['product_quantity'],
                        category=Category(
                            id=row['category_id'],
                            name=row['category_name']
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
                carts.id,
                carts.user_id,
                carts.status,
                cart_items.id cart_item_id,
                cart_items.quantity,
                cart_items.price,
                products.id product_id,
                products.name product_name,
                products.description product_description,
                products.image product_image,
                products.quantity AS product_quantity,
                categories.id category_id,
                categories.name category_name
            FROM carts
            LEFT JOIN cart_items ON carts.id = cart_items.cart_id
            LEFT JOIN products ON cart_items.product_id = products.id
            LEFT JOIN categories ON products.category_id = categories.id
            WHERE carts.id = %s
            """, (cart_id,))
            rows = cur.fetchall()
            cur.close()

            if len(rows) == 0:
                return None

            cart = Cart(id=rows[0]['id'], user_id=rows[0]['user_id'], status=rows[0]['status'], cart_items=[])

            # if cart is empty
            if rows[0]['cart_item_id'] is None:
                return cart

            cart.cart_items = [
                CartItem(
                    id=row['cart_item_id'],
                    quantity=row['quantity'],
                    price=row['price'],
                    product=Product(
                        id=row['product_id'],
                        name=row['product_name'],
                        description=row['product_description'],
                        image=row['product_image'],
                        quantity=row['product_quantity'],
                        category=Category(
                            id=row['category_id'],
                            name=row['category_name']
                        ),
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
            SELECT SUM(cart_items.quantity * cart_items.price) AS subtotal
            FROM cart_items
            WHERE cart_items.cart_id = %s
            """, (cart_id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Cart not found")

            return row['subtotal'] if row['subtotal'] is not None else 0
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_cart_item_quantity(self, cart_item_id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT quantity FROM cart_items WHERE id = %s", (cart_item_id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Cart item not found")

            return row['quantity'] if row['quantity'] is not None else 0
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

            return CartItem(
                id=row['id'],
                cart_id=row['cart_id'],
                product=Product(id=row['product_id']),
                quantity=row['quantity'],
                price=row['price']
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def add_to_cart(self, cart_id: int, product_id: int, quantity: int = 1):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT price, quantity AS stock FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()
            if product is None:
                raise Exception("Product not found")

            if quantity > product['stock']:
                raise Exception(f"Only {product['stock']} item(s) available in stock.")

            # Insert cart item
            cur.execute("""
                INSERT INTO cart_items (cart_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (cart_id, product_id, quantity, product['price']))

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