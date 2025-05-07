from dataclasses import dataclass
from api.models.permission import Permission

@dataclass
class Role:
    id: int = None
    name: str = None
    description: str = None
    permissions: list[Permission] = None
