from typing import Optional
from catalog import SupermarketCatalog
from model_objects import Discount, Offer, Product, SpecialOfferType


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
    discount_amount = round(quantity * unit_price_cents * percentage / 100)
    return Discount(
        product=product,
        description=f"{percentage}% off",
        discount_amount_cents=-discount_amount,
    )


def _create_x_for_y_discount(
    product: Product,
    quantity: float,
    unit_price_cents: int,
    x: int,
    y: int,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int > y:
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
    quantity: float,
    unit_price_cents: int,
    x: int,
    paid_amount_per_x: int,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int >= x:
        total = (
            paid_amount_per_x * (quantity_as_int // x)
            + quantity_as_int % x * unit_price_cents
        )
        discount_amount = unit_price_cents * quantity - total
        return Discount(
            product=product,
            description=f"{x} for {str(paid_amount_per_x)}",
            discount_amount_cents=-discount_amount,
        )


def _create_discount(
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
    elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
        _verify_optional_argument(
            optional_argument=offer.optional_argument,
            offer_type=SpecialOfferType.TEN_PERCENT_DISCOUNT,
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
        raise ValueError(f"Unexpected value for offer.offer_type: {offer.offer_type}")


def create_discounts(
    product_quantities_map: dict[Product, float],
    product_offers_map: dict[Product, Offer],
    catalog: SupermarketCatalog,
) -> list[Discount]:
    discounts: list[Discount] = []

    for product, quantity in product_quantities_map.items():
        if product in product_offers_map.keys():
            offer = product_offers_map[product]
            unit_price_cents = catalog.unit_price_cents(product)
            discount = _create_discount(
                product=product,
                quantity=quantity,
                offer=offer,
                unit_price_cents=unit_price_cents,
            )
            if discount:
                discounts.append(discount)
    return discounts
