from typing import Union
from catalog import SupermarketCatalog
from model_objects import Product, ProductUnit


class IllegalQuantityForProductTypeError(Exception):
    pass


class ProductNotInCatalogError(Exception):
    pass


class ShoppingCart:
    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self._product_quantities: dict[Product, float] = {}

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: Union[int, float]) -> None:
        if product.unit == ProductUnit.EACH and not float(quantity).is_integer():
            raise IllegalQuantityForProductTypeError(
                f"Can't add {quantity} of {product.name} to cart - Products with ProductUnit.EACH must be added in integer quantities!"
            )
        if not self.catalog.contains_product(product=product):
            raise ProductNotInCatalogError(
                f"Can't add Product {product.name} to ShoppingCart - Product is not in Catalog that this ShoppingCart belongs to!"
            )

        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity
