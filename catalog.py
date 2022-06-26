from model_objects import Product


class SupermarketCatalog:
    def add_product(self, product: Product, price_cents: int) -> None:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def contains_product(self, product: Product) -> bool:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def get_unit_price_cents(self, product: Product) -> int:
        raise Exception("cannot be called from a unit test - it accesses the database")
