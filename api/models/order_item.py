from dataclasses import dataclass

@dataclass
class OrderItem:
    id: int = None
    order_id: int = None
    product: Product = None
    quantity: int = None
    price: float = None
