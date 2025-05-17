from dataclasses import dataclass
from api.models.shipping_method import ShippingMethod

@dataclass
class Shipment:
    id: int = None
    recipient_name: str = None
    address: str = None
    phone: str = None
    shipment_method: ShippingMethod = None
    created_at: int = None
    updated_at: int = None
