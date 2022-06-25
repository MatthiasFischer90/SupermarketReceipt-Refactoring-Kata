from model_objects import Offer, Product
from receipt import Receipt
from discount_creation import create_discounts

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
            unit_price_cents = self.catalog.unit_price_cents(product)
            total_price_cents = round(quantity * unit_price_cents)
            receipt.add_product(
                product=product,
                quantity=quantity,
                price_cents=unit_price_cents,
                total_price_cents=total_price_cents,
            )

    def check_out_articles_from_cart(self, cart: ShoppingCart) -> Receipt:
        receipt = Receipt()
        self._add_products_to_receipt(
            receipt=receipt, product_quantities=cart.product_quantities
        )
        discounts = create_discounts(
            product_quantities_map=cart.product_quantities,
            product_offers_map=self.product_offers_map,
            catalog=self.catalog,
        )
        receipt.add_discounts(discounts=discounts)

        return receipt
