from model_objects import Offer, Product, SpecialOfferType
from receipt import Receipt

from shopping_cart import ShoppingCart
from catalog import SupermarketCatalog


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self.product_offers_map: dict[Product, Offer] = {}

    def add_offer(
        self,
        offer: Offer,
    ) -> None:
        self.product_offers_map[offer.product] = offer

    def _add_products_to_receipt(
        self, receipt: Receipt, product_quantities: dict[Product, float]
    ) -> None:
        for product, quantity in product_quantities.items():
            unit_price = self.catalog.unit_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)

    def check_out_articles_from_cart(self, cart: ShoppingCart) -> Receipt:
        receipt = Receipt()
        self._add_products_to_receipt(
            receipt=receipt, product_quantities=cart.product_quantities
        )
        cart.handle_offers(receipt, self.product_offers_map, self.catalog)

        return receipt
