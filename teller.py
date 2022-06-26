from catalog import SupermarketCatalog
from discount_creation import create_discounts
from model_objects import Bundle, Offer, Product
from receipt import Receipt
from shopping_cart import ShoppingCart


class AlreadyHasOfferError(Exception):
    pass


class AlreadyHasBundleError(Exception):
    pass


class Teller:
    """Class that represents the process of checking out items from a ShoppingCart.

    The Teller is associated with a SupermarketCatalog and is aware of all Offers
    and Bundles that are currently active.
    """

    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self.product_offers_map: dict[Product, Offer] = {}
        self.product_bundles_map: dict[Product, Bundle] = {}

    def add_offer(
        self,
        offer: Offer,
    ) -> None:
        """Add Offer to the Teller instance.

        Every Offer added to the Teller will later be used when the Teller creates Receipts.

        Args:
            offer (Offer): The Offer to add to the Teller.

        Raises:
            AlreadyHasOfferError: Raised if the Offer is for a Product for which the Teller
            already has an Offer.
            AlreadyHasBundleError: Raised if the Offer is for a Product for which the Teller
            already has a Bundle.
        """

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
        """Add Bundle to the Teller instance.

        Every Bundle added to the Teller will later be used when the Teller creates Receipts.

        Args:
            offer (Offer): The Bundle to add to the Teller.

        Raises:
            AlreadyHasOfferError: Raised if the Bundle is for a Product for which the Teller
            already has an Offer.
            AlreadyHasBundleError: Raised if the Bundle is for a Product for which the Teller
            already has a Bundle.
        """

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
        """Check out the items from a given ShoppingCart and return a Receipt.

        In order to create a Receipt, this method:
            - calculates the prices of all Products given via the ShoppingCart
            - infers all Discounts for the Products (using the Offers and Bundles
              stored by the Teller)

        Args:
            cart (ShoppingCart): The ShoppingCart whose Products are to be used for
            the Receipt creation.

        Returns:
            Receipt: The Receipt created from the given ShoppingCart.
        """

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
