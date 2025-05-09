from dataclasses import dataclass, field
from api.models.user import User
from api.models.cart import Cart
from api.models.order_item import OrderItem
from api.models.shipment import Shipment

@dataclass
class Order:
    id: int = None
    user: User = None
    cart: Cart = None
    order_items: list[OrderItem] = field(default_factory=list)
    shipment: Shipment = None
    created_at: int = None
    updated_at: int = None
