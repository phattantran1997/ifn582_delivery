from dataclasses import dataclass
from api.models.product import Product

@dataclass
class CartItem:
    id: int = None
    cart_id: int = None
    product: Product = None
    quantity: int = 1
    price: float = 0
