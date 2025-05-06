from dataclasses import dataclass

@dataclass
class Product:
    id: int = None
    name: str = None
    price: float = None
    category_id: int = None
