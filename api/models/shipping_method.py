from dataclasses import dataclass

@dataclass
class ShippingMethod:
    id: int = None
    name: str = None
    description: str = None
