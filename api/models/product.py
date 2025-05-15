from dataclasses import dataclass
from api.models.category import Category

@dataclass
class Product:
    id: int = None
    name: str = None
    price: float = None
    image: str = ""
    category: Category = None
