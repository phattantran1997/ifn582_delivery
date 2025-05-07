from dataclasses import dataclass
from api.models.shipping_method import ShippingMethod

@dataclass
class Shipment:
    id: int = None
    address: str = None
    phone: str = None
    shipment_method: ShipmentMethod = None
    created_at: int = None
    updated_at: int = None
