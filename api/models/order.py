from dataclasses import dataclass, field
from api.models.order_item import OrderItem
from api.models.shipment import Shipment

@dataclass
class Order:
    id: int = None
    user_id: int = None
    cart_id: int = None
    status: str = None
    items: list[OrderItem] = field(default_factory=list)
    shipment: Shipment = None
    total_amount: float = None
    created_at: int = None
    updated_at: int = None
