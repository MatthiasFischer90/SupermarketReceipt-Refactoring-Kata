from collections import namedtuple
from typing import Optional, Union
from catalog import SupermarketCatalog
from model_objects import (
    Bundle,
    Discount,
    Offer,
    Product,
    ProductUnit,
    SpecialOfferType,
)


BundleDiscountItem = namedtuple(
    "BundleDiscountItem", "product quantity unit_price_cents"
)


class InvalidProductUnitError(Exception):
    pass


def _verify_optional_argument(
    optional_argument: Optional[float], offer_type: SpecialOfferType
) -> None:
    if optional_argument is None:
        raise ValueError(
            f"optional_argument can not be None for Offer of type {offer_type}!"
        )


def _create_percentage_discount(
    product: Product, quantity: float, unit_price_cents: int, percentage: float
) -> Discount:
    if percentage < 0 or percentage > 100:
        raise ValueError(
            f"Discount percentage must be between 0 and 100, but got {percentage}!"
        )
    discount_amount = round(quantity * unit_price_cents * percentage / 100)
    return Discount(
        product=product,
        description=f"{percentage}% off",
        discount_amount_cents=-discount_amount,
    )


def _create_x_for_y_discount(
    product: Product,
    quantity: Union[int, float],
    unit_price_cents: int,
    x: int,
    y: int,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int <= y:
        return None

    if x <= y:
        raise ValueError(
            f"Discounted quantity {x} must be higher than paid quantity {y}!"
        )
    discount_amount = quantity * unit_price_cents - (
        ((quantity_as_int // x) * y * unit_price_cents)
        + quantity_as_int % x * unit_price_cents
    )
    return Discount(
        product=product,
        description=f"{x} for {y}",
        discount_amount_cents=-discount_amount,
    )


def _create_x_for_amount_discount(
    product: Product,
    quantity: Union[int, float],
    unit_price_cents: int,
    x: int,
    paid_amount_per_x: int,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int < x:
        return None

    if paid_amount_per_x >= unit_price_cents * x:
        raise ValueError(
            f'Discount "{x} for {paid_amount_per_x}" must be lower than {x} times the unit price of {unit_price_cents} = {unit_price_cents * x} by itself!'
        )
    total = (
        paid_amount_per_x * (quantity_as_int // x)
        + quantity_as_int % x * unit_price_cents
    )
    discount_amount = unit_price_cents * quantity - total
    return Discount(
        product=product,
        description=f"{x} for {paid_amount_per_x}",
        discount_amount_cents=-discount_amount,
    )


def _create_discount_from_offer(
    product: Product, quantity: float, offer: Offer, unit_price_cents: int
) -> Optional[Discount]:
    if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
        return _create_x_for_y_discount(
            product=product,
            quantity=quantity,
            unit_price_cents=unit_price_cents,
            x=3,
            y=2,
        )
    elif offer.offer_type == SpecialOfferType.PERCENT_DISCOUNT:
        _verify_optional_argument(
            optional_argument=offer.optional_argument,
            offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        )
        return _create_percentage_discount(
            product=product,
            quantity=quantity,
            unit_price_cents=unit_price_cents,
            percentage=offer.optional_argument,
        )
    elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
        _verify_optional_argument(
            optional_argument=offer.optional_argument,
            offer_type=SpecialOfferType.TWO_FOR_AMOUNT,
        )
        return _create_x_for_amount_discount(
            product=product,
            quantity=quantity,
            unit_price_cents=unit_price_cents,
            x=2,
            paid_amount_per_x=offer.optional_argument,
        )
    elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
        _verify_optional_argument(
            optional_argument=offer.optional_argument,
            offer_type=SpecialOfferType.FIVE_FOR_AMOUNT,
        )
        return _create_x_for_amount_discount(
            product=product,
            quantity=quantity,
            unit_price_cents=unit_price_cents,
            x=5,
            paid_amount_per_x=offer.optional_argument,
        )
    else:
        raise ValueError(f"Unexpected value for offer.offer_type: {offer.offer_type}!")


def _create_discounts_from_offers(
    product_quantities_map: dict[Product, float],
    product_offers_map: dict[Product, Offer],
    catalog: SupermarketCatalog,
) -> list[Discount]:
    discounts: list[Discount] = []
    for product, quantity in product_quantities_map.items():
        if product not in product_offers_map.keys():
            continue

        offer = product_offers_map[product]
        unit_price_cents = catalog.get_unit_price_cents(product)
        discount = _create_discount_from_offer(
            product=product,
            quantity=quantity,
            offer=offer,
            unit_price_cents=unit_price_cents,
        )
        if discount:
            discounts.append(discount)
    return discounts


def _create_discounts_from_bundle(
    bundle: Bundle,
    lowest_purchase_quantity: int,
    bundle_discount_items: list[BundleDiscountItem],
) -> list[Discount]:
    discounts: list[Discount] = []
    if lowest_purchase_quantity <= 0:
        raise ValueError(
            f"lowest_purchase_quantity must be greater than 0, but it's {lowest_purchase_quantity}!"
        )

    for bundle_discount_item in bundle_discount_items:
        quantity = bundle_discount_item.quantity
        unit_price_cents = bundle_discount_item.unit_price_cents
        discount_amount = quantity * unit_price_cents - (
            round(
                lowest_purchase_quantity
                * ((100 - bundle.discount_percentage) / 100)
                * unit_price_cents
            )
            + (quantity - lowest_purchase_quantity) * unit_price_cents
        )
        discounts.append(
            Discount(
                product=bundle_discount_item.product,
                description=f"Bundle discount: {bundle.discount_percentage}% off",
                discount_amount_cents=-discount_amount,
            )
        )
    return discounts


def _create_discounts_from_bundles(
    product_quantities_map: dict[Product, float],
    bundles: list[Bundle],
    catalog: SupermarketCatalog,
) -> list[Discount]:
    discounts: list[Discount] = []
    for bundle in bundles:
        found_unpurchased_bundle_product = False
        lowest_purchase_quantity: int = -1
        for product in bundle.products:
            # Bundles can only be applied if every Product has ProductUnit.EACH
            if product.unit != ProductUnit.EACH:
                raise InvalidProductUnitError(
                    f"Bundles can only be applied if every Product has ProductUnit.EACH, but {product.name} has {product.unit}!"
                )

            product_purchase_quantity = product_quantities_map.get(product)
            if product_purchase_quantity is None:
                found_unpurchased_bundle_product = True
                break

            # determine the lowest quantity of any bought product in the bundle, so we know how much
            # to apply the bundle for
            if (
                product_purchase_quantity < lowest_purchase_quantity
                or lowest_purchase_quantity == -1
            ):
                lowest_purchase_quantity = product_purchase_quantity

        if found_unpurchased_bundle_product:
            break

        discounts += _create_discounts_from_bundle(
            bundle=bundle,
            lowest_purchase_quantity=lowest_purchase_quantity,
            bundle_discount_items=[
                BundleDiscountItem(
                    product=product,
                    quantity=product_quantities_map.get(product),
                    unit_price_cents=catalog.get_unit_price_cents(product),
                )
                for product in bundle.products
            ],
        )
    return discounts


def create_discounts(
    product_quantities_map: dict[Product, float],
    product_offers_map: dict[Product, Offer],
    bundles: list[Bundle],
    catalog: SupermarketCatalog,
) -> list[Discount]:
    discounts = _create_discounts_from_offers(
        product_quantities_map=product_quantities_map,
        product_offers_map=product_offers_map,
        catalog=catalog,
    )
    discounts += _create_discounts_from_bundles(
        product_quantities_map=product_quantities_map,
        bundles=bundles,
        catalog=catalog,
    )
    return discounts
