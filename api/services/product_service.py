from api.services.base_service import BaseService
from api.models.category import Category
from api.models.product import Product

class ProductService(BaseService):
    def get_all_products(self):
        try:
            cur = self.get_cursor()
            cur.execute("""
                SELECT p.id, p.name, p.price, p.category_id, c.name AS category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.id
            """)
            products = cur.fetchall()
            cur.close()

            return [
                Product(
                    id=row[0],
                    name=row[1],
                    price=float(row[2]),
                    category=Category(id=row[3], name=row[4])
                )
                for row in products
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_product_by_id(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
                SELECT p.id, p.name, p.price, p.category_id, c.name AS category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """, (id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Product not found")

            return Product(
                id=row[0],
                name=row[1],
                price=float(row[2]),
                category=Category(id=row[3], name=row[4])
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def create_product(self, data: dict):
        try:
            required_fields = ['name', 'price', 'category_id']
            for field in required_fields:
                if field not in data:
                    raise Exception(f"Missing required field: {field}")

            cur = self.get_cursor()
            cur.execute(
                "INSERT INTO products (name, price, category_id) VALUES (%s, %s, %s)",
                (data['name'], data['price'], data['category_id'])
            )
            self.mysql.connection.commit()
            product_id = cur.lastrowid
            cur.close()

            return self.get_product_by_id(product_id)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def update_product(self, id: int, data: dict):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cur.fetchone()
            if row is None:
                cur.close()
                raise Exception("Product not found")

            update_fields = []
            values = []
            for field in ['name', 'price', 'category_id']:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    values.append(data[field])

            if not update_fields:
                cur.close()
                raise Exception("No fields to update")

            values.append(id)
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)
            self.mysql.connection.commit()
            cur.close()

            return self.get_product_by_id(id)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def delete_product(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cur.fetchone()
            if row is None:
                cur.close()
                raise Exception("Product not found")

            cur.execute("DELETE FROM products WHERE id = %s", (id,))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_categories(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM categories")
            categories = cur.fetchall()
            cur.close()

            return [
                Category(id=row[0], name=row[1])
                for row in categories
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
