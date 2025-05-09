from enum import Enum
from dataclasses import dataclass, field

from api.models.cart_items import CartItem

class CartStatus(str, Enum):
    ACTIVE = 'active'
    ABANDONED = 'abandoned'

@dataclass
class Cart:
    id: int = None
    user_id: int = None
    status: CartStatus = CartStatus.ACTIVE
    cart_items: list[CartItem] = field(default_factory=list)
    created_at: int = None
    updated_at: int = None

# Usage:
# Cart = Cart(status=CartStatus.ABANDONED)
# print(Cart.status.value)
