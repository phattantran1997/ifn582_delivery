from api.services.base_service import BaseService
from api.models.user import User

class UserService(BaseService):
    def get_all_users(self):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            cur.close()

            return [
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email']
                )
                for row in users
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_user_by_id(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cur.fetchone()
            cur.close()

            if user is None:
                raise Exception("User not found")

            return User(
                id=user['id'],
                username=user['username'],
                email=user['email']
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def update_user(self, id: int, data: dict):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            if not cur.fetchone():
                cur.close()
                raise Exception("User not found")

            update_fields = []
            values = []
            for field in ['username', 'email']:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    values.append(data[field])

            if not update_fields:
                cur.close()
                raise Exception("No fields to update")

            values.append(id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)
            self.mysql.connection.commit()
            cur.close()

            return self.get_user_by_id(id)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def delete_user(self, id: int):
        try:
            cur = self.get_cursor()
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            if not cur.fetchone():
                cur.close()
                raise Exception("User not found")

            cur.execute("DELETE FROM users WHERE id = %s", (id,))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
