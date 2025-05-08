import hashlib

from api.services.base_service import BaseService

class AuthService(BaseService):
    def login(self, data):
        try:
            cur = self.get_cursor()
            # SQL Injection prevention wrapper (?)
            cur.execute(
                "SELECT * FROM users WHERE username = (?) AND password = (?)",
                (data['username'], data['password'])
            )
            user = cur.fetchone()
            cur.close()

            if user:
                return user
            else:
                raise Exception("User not found")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def register(self, data):
        password_hash = self.hash_password(data['password'])
        try:
            cur = self.get_cursor()
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (data['username'], data['email'], password_hash)
            )
            self.mysql.connection.commit()
            cur.close()

            return data
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    