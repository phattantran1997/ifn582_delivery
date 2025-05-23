from api.services.base_service import BaseService
from api.models.category import Category
from api.models.product import Product

class ProductService(BaseService):
    def get_all_products(self, category=None, search=None):
        try:
            cur = self.get_cursor()
            query = """
                SELECT p.id, p.name, p.price, p.image, p.description, p.category_id, c.name AS category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE 1=1
            """
            params = []

            if category:
                query += " AND c.name = %s"
                params.append(category)

            if search:
                query += " AND (p.name LIKE %s OR p.description LIKE %s OR c.name LIKE %s)"
                search_term = f"%{search}%"
                params.extend([search_term, search_term, search_term])

            query += " ORDER BY p.id"
            
            cur.execute(query, params)
            products = cur.fetchall()
            cur.close()

            return [
                Product(
                    id=row['id'],
                    name=row['name'],
                    price=float(row['price']),
                    image=row['image'],
                    description=row['description'],
                    category=Category(id=row['category_id'], name=row['category_name'])
                )
                for row in products
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_product_by_id(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("""
                SELECT p.id, p.name, p.price, p.image, p.description, p.category_id, c.name AS category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """, (id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Product not found")

            return Product(
                id=row['id'],
                name=row['name'],
                price=float(row['price']),
                image=row['image'],
                description=row['description'],
                category=Category(id=row['category_id'], name=row['category_name'])
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
                "INSERT INTO products (name, price, category_id, image, description) VALUES (%s, %s, %s, %s, %s)",
                (data['name'], data['price'], data['category_id'], data['image'], data['description'])
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
            for field in ['name', 'price', 'category_id', 'image', 'description']:
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
                Category(
                    id=row['id'], 
                    name=row['name']
                )
                for row in categories
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_category_by_id(self, id):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM categories WHERE id = %s", (id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                raise Exception("Category not found")

            return Category(
                id=row['id'], 
                name=row['name']
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    def create_category(self, name):
        try:
            cur = self.get_cursor()
            cur.execute(
                "INSERT INTO categories (name) VALUES (%s)",
                (name,)
            )
            self.mysql.connection.commit()
            category_id = cur.lastrowid
            cur.close()

            return self.get_category_by_id(category_id)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")


    def update_category(self, id, name):
        try:
            cur = self.get_cursor()
            cur.execute("UPDATE categories SET name = %s WHERE id = %s", (name, id))
            self.mysql.connection.commit()
            cur.close()
            return self.get_category_by_id(id)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")    
        
