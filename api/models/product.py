from dataclasses import dataclass
from enum import Enum
from api.models.category import Category

class ProductStatus(str, Enum):
    IN_STOCK = 'in_stock'
    OUT_OF_STOCK = 'out_of_stock'

@dataclass
class Product:
    id: int = None
    name: str = None
    price: float = None
    image: str = ""
    category: Category = None
    description: str = ""
    availability: ProductStatus = ProductStatus.IN_STOCK   
    quantity: int = 0
