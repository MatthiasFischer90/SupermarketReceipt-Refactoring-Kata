from model_objects import Bundle, Offer, Product
from receipt import Receipt
from discount_creation import create_discounts

from shopping_cart import ShoppingCart
from catalog import SupermarketCatalog


class AlreadyHasOfferError(Exception):
    pass


class AlreadyHasBundleError(Exception):
    pass


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self.product_offers_map: dict[Product, Offer] = {}
        self.product_bundles_map: dict[Product, Bundle] = {}

    def add_offer(
        self,
        offer: Offer,
    ) -> None:
        product = offer.product
        if product in self.product_offers_map:
            raise AlreadyHasOfferError(
                f"Can't add Offer for {product}: Product already has an Offer!"
            )
        if product in self.product_bundles_map:
            raise AlreadyHasBundleError(
                f"Can't add Offer for {product}: Product already has a Bundle!"
            )
        self.product_offers_map[offer.product] = offer

    def add_bundle(
        self,
        bundle: Bundle,
    ) -> None:
        for product in bundle.products:
            if product in self.product_offers_map:
                raise AlreadyHasOfferError(
                    f"Can't add Bundle for {product}: Product already has an Offer!"
                )
            if product in self.product_bundles_map:
                raise AlreadyHasBundleError(
                    f"Can't add Bundle for {product}: Product already has a Bundle!"
                )

        for product in bundle.products:
            self.product_bundles_map[product] = bundle

    def _add_products_to_receipt(
        self, receipt: Receipt, product_quantities: dict[Product, float]
    ) -> None:
        for product, quantity in product_quantities.items():
            unit_price_cents = self.catalog.get_unit_price_cents(product)
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
        # To get a list of all Bundles, we can take all the values in
        # self.product_bundles_map. To make them unique, convert the
        # list of Bundles into a set and then back into a list
        bundles = list(set(self.product_bundles_map.values()))
        discounts = create_discounts(
            product_quantities_map=cart.product_quantities,
            product_offers_map=self.product_offers_map,
            bundles=bundles,
            catalog=self.catalog,
        )
        receipt.add_discounts(discounts=discounts)

        return receipt
