import math

from catalog import SupermarketCatalog
from model_objects import Offer, Product, SpecialOfferType, Discount
from receipt import Receipt


class ShoppingCart:
    def __init__(self):
        self._product_quantities: dict[Product, float] = {}

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        if product in self._product_quantities.keys():
            self._product_quantities[product] = (
                self._product_quantities[product] + quantity
            )
        else:
            self._product_quantities[product] = quantity
