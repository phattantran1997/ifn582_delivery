from api.services.base_service import BaseService

class ProductService(BaseService):
    def get_all_products(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'price': float(row[2]),
                    'category_id': row[3]
                }
                for row in products
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_product_by_id(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (id,))
            product = cur.fetchone()
            cur.close()

            if product is None:
                raise Exception("Product not found")

            return {
                'id': product[0],
                'name': product[1],
                'price': float(product[2]),
                'category_id': product[3]
            }
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
            if not cur.fetchone():
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
            if not cur.fetchone():
                cur.close()
                raise Exception("Product not found")

            cur.execute("DELETE FROM products WHERE id = %s", (id,))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
