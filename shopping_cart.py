from typing import Union
from model_objects import Product, ProductUnit


class ShoppingCart:
    def __init__(self):
        self._product_quantities: dict[Product, float] = {}

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: Union[int, float]) -> None:
        if product.unit == ProductUnit.EACH and not float(quantity).is_integer():
            raise ValueError(
                f"Can't add {quantity} of {product.name} to cart - Products with ProductUnit.EACH must be added in integer quantities!"
            )

        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity
