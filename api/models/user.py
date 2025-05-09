from dataclasses import dataclass
from api.models.role import Role

@dataclass
class User:
    id: int = None
    username: str = None
    email: str = None
    password: str = None
    role: Role = None
    last_login_at: int = None
    created_at: int = None
    updated_at: int = None
