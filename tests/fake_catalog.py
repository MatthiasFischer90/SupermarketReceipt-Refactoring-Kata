from catalog import SupermarketCatalog
from model_objects import Product


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products: dict[str, Product] = {}
        self.prices: dict[str, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product: Product) -> float:
        return self.prices[product.name]
