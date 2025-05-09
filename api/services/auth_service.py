import hashlib

from api.models.role import Role
from api.models.user import User
from api.services.base_service import BaseService

class AuthService(BaseService):
    def login(self, data):
        try:
            cur = self.get_cursor()
            # SQL Injection prevention wrapper (?)
            cur.execute("""
                SELECT 
                    u.id, u.username, u.email, u.password, u.last_login_at, u.created_at, u.updated_at,
                    r.id AS role_id, r.name AS role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.email = (%s);
            """, (data['email'],))
            row = cur.fetchone()
            cur.close()

            if row:
                return User(**{
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password': row[3],
                    'role': Role(id=row[4], name=row[5]),
                    'last_login_at': row[6],
                    'created_at': row[7],
                    'updated_at': row[8],
                })

            return None
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def register(self, data):
        password_hash = self.hash_password(data['password'])
        try:
            cur = self.get_cursor()
            cur.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s);",
                (data['email'], password_hash)
            )
            self.mysql.connection.commit()
            cur.close()

            return User(**data)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password, hash):
        return self.hash_password(password) == hash
