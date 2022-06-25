from catalog import SupermarketCatalog
from model_objects import Product


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products: dict[str, Product] = {}
        self.prices_cents: dict[str, int] = {}

    def add_product(self, product: Product, price_cents: int) -> None:
        self.products[product.name] = product
        self.prices_cents[product.name] = price_cents

    def get_unit_price_cents(self, product: Product) -> int:
        return self.prices_cents[product.name]
