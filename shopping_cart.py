from model_objects import Product


class ShoppingCart:
    def __init__(self):
        self._product_quantities: dict[Product, float] = {}

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity
