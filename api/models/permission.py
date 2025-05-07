from dataclasses import dataclass

@dataclass
class Permission:
    id: int = None
    name: str = None
    description: str = None
