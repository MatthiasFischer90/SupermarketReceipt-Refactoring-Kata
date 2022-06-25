from enum import Enum
from typing import Optional


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class Product:
    def __init__(self, name: str, unit: ProductUnit):
        self.name = name
        self.unit = unit


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


class Offer:
    def __init__(
        self,
        offer_type: SpecialOfferType,
        product: Product,
        optional_argument: Optional[float],
    ):
        self.offer_type = offer_type
        self.product = product
        self.optional_argument = optional_argument


class Discount:
    def __init__(self, product: Product, description: str, discount_amount: float):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount
