from dataclasses import dataclass
from api.models.product import Product

@dataclass
class OrderItem:
    id: int = None
    order_id: int = None
    product_id: int = None
    product: Product = None
    quantity: int = None
    price: float = None
