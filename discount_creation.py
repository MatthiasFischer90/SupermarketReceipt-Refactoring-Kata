from typing import Optional
from catalog import SupermarketCatalog
from model_objects import Discount, Offer, Product, SpecialOfferType


def _create_percentage_discount(
    product: Product, quantity: float, unit_price: float, percentage: float
) -> Discount:
    discount_amount = quantity * unit_price * percentage / 100.0
    return Discount(
        product=product,
        description=str(percentage) + "% off",
        discount_amount=-discount_amount,
    )


def _create_x_for_y_discount(
    product: Product,
    quantity: float,
    unit_price: float,
    x: int,
    y: int,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int > y:
        discount_amount = quantity * unit_price - (
            ((quantity_as_int // x) * y * unit_price) + quantity_as_int % x * unit_price
        )
        return Discount(
            product=product,
            description=f"{x} for {y}",
            discount_amount=-discount_amount,
        )


def _create_x_for_amount_discount(
    product: Product,
    quantity: float,
    unit_price: float,
    x: int,
    paid_amount_per_x: float,
) -> Optional[Discount]:
    quantity_as_int = int(quantity)
    if quantity_as_int >= x:
        total = (
            paid_amount_per_x * (quantity_as_int // x)
            + quantity_as_int % x * unit_price
        )
        discount_amount = unit_price * quantity - total
        return Discount(
            product=product,
            description=f"{x} for {str(paid_amount_per_x)}",
            discount_amount=-discount_amount,
        )


def _create_discount(
    product: Product, quantity: float, offer: Offer, unit_price: float
) -> Optional[Discount]:
    if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
        return _create_x_for_y_discount(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            x=3,
            y=2,
        )
    elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
        return _create_percentage_discount(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            percentage=offer.argument,
        )
    elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
        return _create_x_for_amount_discount(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            x=2,
            paid_amount_per_x=offer.argument,
        )
    elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
        return _create_x_for_amount_discount(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            x=5,
            paid_amount_per_x=offer.argument,
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
            unit_price = catalog.unit_price(product)
            discount = _create_discount(
                product=product,
                quantity=quantity,
                offer=offer,
                unit_price=unit_price,
            )
            if discount:
                discounts.append(discount)
    return discounts
