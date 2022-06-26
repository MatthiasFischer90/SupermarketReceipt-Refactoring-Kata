import pytest

from discount_creation import (
    BundleDiscountItem,
    InvalidProductUnitError,
    _verify_optional_argument,
    _create_percentage_discount,
    _create_x_for_y_discount,
    _create_x_for_amount_discount,
    _create_discount_from_offer,
    _create_discounts_from_bundle,
    _create_discounts_from_offers,
    _create_discounts_from_bundles,
    create_discounts,
)
from model_objects import Bundle, Offer, Product, ProductUnit, SpecialOfferType
from tests.fake_catalog import FakeCatalog


def test_verify_optional_argument():
    _verify_optional_argument(
        optional_argument=20, offer_type=SpecialOfferType.PERCENT_DISCOUNT
    )


def test_fail_verify_optional_argument():
    with pytest.raises(
        ValueError,
        match="optional_argument can not be None for Offer of type SpecialOfferType.PERCENT_DISCOUNT!",
    ):
        _verify_optional_argument(
            optional_argument=None, offer_type=SpecialOfferType.PERCENT_DISCOUNT
        )


def test_create_percentage_discount_0_percent():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_percentage_discount(
        product=apples, quantity=2.5, unit_price_cents=199, percentage=0
    )
    assert "0% off" == discount.description
    assert 0 == discount.discount_amount_cents


def test_create_percentage_discount_20_percent():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_percentage_discount(
        product=apples, quantity=2.5, unit_price_cents=199, percentage=20
    )
    assert "20% off" == discount.description
    assert -100 == discount.discount_amount_cents


def test_create_percentage_discount_100_percent():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_percentage_discount(
        product=apples, quantity=2.5, unit_price_cents=199, percentage=100
    )
    assert "100% off" == discount.description
    assert -498 == discount.discount_amount_cents


def test_fail_create_percentage_discount_negative_percent():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    with pytest.raises(
        ValueError, match="Discount percentage must be between 0 and 100, but got -10!"
    ):
        _create_percentage_discount(
            product=apples, quantity=2.5, unit_price_cents=199, percentage=-10
        )


def test_fail_create_percentage_discount_more_than_100_percent():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    with pytest.raises(
        ValueError, match="Discount percentage must be between 0 and 100, but got 120!"
    ):
        _create_percentage_discount(
            product=apples, quantity=2.5, unit_price_cents=199, percentage=120
        )


def test_create_x_for_y_discount_5_for_3_and_buy_6():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_x_for_y_discount(
        product=apples,
        quantity=6,
        unit_price_cents=199,
        x=5,
        y=3,
    )
    assert "5 for 3" == discount.description
    assert -398 == discount.discount_amount_cents


def test_create_x_for_y_discount_5_for_3_and_buy_11():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_x_for_y_discount(
        product=apples,
        quantity=11,
        unit_price_cents=199,
        x=5,
        y=3,
    )
    assert "5 for 3" == discount.description
    assert -796 == discount.discount_amount_cents


def test_create_x_for_y_discount_5_for_3_and_buy_2():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_x_for_y_discount(
        product=apples,
        quantity=2,
        unit_price_cents=199,
        x=5,
        y=3,
    )
    assert None == discount


def test_fail_create_x_for_y_discount_3_for_3():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    with pytest.raises(
        ValueError, match="Discounted quantity 3 must be higher than paid quantity 3!"
    ):
        _create_x_for_y_discount(
            product=apples,
            quantity=5,
            unit_price_cents=199,
            x=3,
            y=3,
        )


def test_create_x_for_amount_discount_3_for_400_and_buy_4():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_x_for_amount_discount(
        product=apples, quantity=4, unit_price_cents=199, x=3, paid_amount_per_x=400
    )
    assert "3 for 400" == discount.description
    assert -197 == discount.discount_amount_cents


def test_create_x_for_amount_discount_3_for_400_and_buy_2():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    discount = _create_x_for_amount_discount(
        product=apples, quantity=2, unit_price_cents=199, x=3, paid_amount_per_x=400
    )
    assert None == discount


def test_fail_create_x_for_amount_discount_amount_too_high():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    with pytest.raises(
        ValueError,
        match='Discount "3 for 597" must be lower than 3 times the unit price of 199 \(= 597\) by itself!',
    ):
        _create_x_for_amount_discount(
            product=apples,
            quantity=5,
            unit_price_cents=199,
            x=3,
            paid_amount_per_x=597,
        )


def test_create_discount_from_offer(mocker):
    apples = Product(name="apples", unit=ProductUnit.KILO)

    mocked_create_x_for_y_discount = mocker.patch(
        "discount_creation._create_x_for_y_discount"
    )
    _create_discount_from_offer(
        product=apples,
        quantity=5.5,
        offer=Offer(
            offer_type=SpecialOfferType.THREE_FOR_TWO,
            product=apples,
            optional_argument=None,
        ),
        unit_price_cents=199,
    )
    mocked_create_x_for_y_discount.assert_called_with(
        product=apples, quantity=5.5, unit_price_cents=199, x=3, y=2
    )

    mocked_create_percentage_discount = mocker.patch(
        "discount_creation._create_percentage_discount"
    )
    _create_discount_from_offer(
        product=apples,
        quantity=5.5,
        offer=Offer(
            offer_type=SpecialOfferType.PERCENT_DISCOUNT,
            product=apples,
            optional_argument=20,
        ),
        unit_price_cents=199,
    )
    mocked_create_percentage_discount.assert_called_with(
        product=apples, quantity=5.5, unit_price_cents=199, percentage=20
    )

    # TWO_FOR_AMOUNT and FIVE_FOR_AMOUNT use the same mocker
    mocked_x_for_amount_discount = mocker.patch(
        "discount_creation._create_x_for_amount_discount"
    )
    _create_discount_from_offer(
        product=apples,
        quantity=5.5,
        offer=Offer(
            offer_type=SpecialOfferType.TWO_FOR_AMOUNT,
            product=apples,
            optional_argument=150,
        ),
        unit_price_cents=199,
    )
    mocked_x_for_amount_discount.assert_called_with(
        product=apples, quantity=5.5, unit_price_cents=199, x=2, paid_amount_per_x=150
    )

    _create_discount_from_offer(
        product=apples,
        quantity=5.5,
        offer=Offer(
            offer_type=SpecialOfferType.FIVE_FOR_AMOUNT,
            product=apples,
            optional_argument=800,
        ),
        unit_price_cents=199,
    )
    mocked_x_for_amount_discount.assert_called_with(
        product=apples, quantity=5.5, unit_price_cents=199, x=5, paid_amount_per_x=800
    )


def test_fail_create_discount_from_offer_invalid_type():
    apples = Product(name="apples", unit=ProductUnit.KILO)
    invalid_offer_type = -500
    with pytest.raises(
        ValueError,
        match="Unexpected value for offer.offer_type: -500!",
    ):
        _create_discount_from_offer(
            product=apples,
            quantity=5.5,
            offer=Offer(
                offer_type=invalid_offer_type,
                product=apples,
                optional_argument=150,
            ),
            unit_price_cents=199,
        )


def test_create_discounts_from_offers():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=99)
    # toothbrushes are purchased and have an offer, and a discount is applied to the offer
    toothbrush_offer = Offer(
        offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        product=toothbrush,
        optional_argument=10,
    )

    # apples are purchased and have an offer, but no discount is applied (not enough bought to trigger the discount)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=199)
    apples_offer = Offer(
        offer_type=SpecialOfferType.THREE_FOR_TWO,
        product=toothbrush,
        optional_argument=None,
    )

    # melons are purchased, but they don't have an offer, so no discount is applied
    melon = Product(name="melon", unit=ProductUnit.EACH)
    catalog.add_product(product=melon, price_cents=210)

    discounts = _create_discounts_from_offers(
        product_quantities_map={toothbrush: 2, apples: 2, melon: 2},
        product_offers_map={
            toothbrush: toothbrush_offer,
            apples: apples_offer,
        },
        catalog=catalog,
    )
    assert 1 == len(discounts)
    discount_toothbrush = discounts[0]
    assert toothbrush == discount_toothbrush.product
    assert "10% off" == discount_toothbrush.description
    assert -20 == discount_toothbrush.discount_amount_cents


def test_create_discounts_from_bundle():
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    discount_toothbrush, discount_toothpaste = _create_discounts_from_bundle(
        bundle=bundle,
        lowest_purchase_quantity=2,
        bundle_discount_items=[
            BundleDiscountItem(product=toothbrush, quantity=2, unit_price_cents=100),
            BundleDiscountItem(product=toothpaste, quantity=3, unit_price_cents=80),
        ],
    )
    assert toothbrush == discount_toothbrush.product
    assert "Bundle discount: 20% off" == discount_toothbrush.description
    assert -40 == discount_toothbrush.discount_amount_cents
    assert toothpaste == discount_toothpaste.product
    assert "Bundle discount: 20% off" == discount_toothpaste.description
    assert -32 == discount_toothpaste.discount_amount_cents


def test_fail_create_discounts_from_bundle_lowest_purchase_quantity_is_0():
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    with pytest.raises(
        ValueError,
        match="lowest_purchase_quantity must be greater than 0, but it's 0!",
    ):
        _create_discounts_from_bundle(
            bundle=bundle,
            lowest_purchase_quantity=0,
            bundle_discount_items=[
                BundleDiscountItem(
                    product=toothbrush, quantity=2, unit_price_cents=100
                ),
                BundleDiscountItem(product=toothpaste, quantity=3, unit_price_cents=80),
            ],
        )


def test_fail_create_discounts_from_bundle_lowest_purchase_quantity_is_minus_2():
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    with pytest.raises(
        ValueError,
        match="lowest_purchase_quantity must be greater than 0, but it's -2!",
    ):
        _create_discounts_from_bundle(
            bundle=bundle,
            lowest_purchase_quantity=-2,
            bundle_discount_items=[
                BundleDiscountItem(
                    product=toothbrush, quantity=2, unit_price_cents=100
                ),
                BundleDiscountItem(product=toothpaste, quantity=3, unit_price_cents=80),
            ],
        )


def test_create_discounts_from_bundles():
    catalog = FakeCatalog()

    # dental bundle
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=99)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    dental_bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )

    # car bundle
    oil_can = Product(name="oil can", unit=ProductUnit.EACH)
    catalog.add_product(product=oil_can, price_cents=400)

    # wheels are part of the car bundle, but not a single wheel is bought
    wheel = Product(name="wheel", unit=ProductUnit.EACH)
    catalog.add_product(product=wheel, price_cents=50000)

    car_bundle = Bundle(
        products=[oil_can, wheel],
        discount_percentage=15,
    )

    discounts = _create_discounts_from_bundles(
        product_quantities_map={toothbrush: 2, toothpaste: 3, oil_can: 2},
        bundles=[dental_bundle, car_bundle],
        catalog=catalog,
    )
    assert 2 == len(discounts)
    discount_toothbrush, discount_toothpaste = discounts
    assert toothbrush == discount_toothbrush.product
    assert "Bundle discount: 20% off" == discount_toothbrush.description
    assert -40 == discount_toothbrush.discount_amount_cents
    assert toothpaste == discount_toothpaste.product
    assert "Bundle discount: 20% off" == discount_toothpaste.description
    assert -32 == discount_toothpaste.discount_amount_cents


def test_create_discounts_from_bundles_with_empty_list_of_bundles():
    catalog = FakeCatalog()

    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=99)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    discounts = _create_discounts_from_bundles(
        product_quantities_map={toothbrush: 2, toothpaste: 3},
        bundles=[],
        catalog=catalog,
    )
    assert 0 == len(discounts)


def test_fail_create_discounts_from_bundles_invalid_type():
    catalog = FakeCatalog()

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=99)

    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=80)

    bundle = Bundle(
        products=[apples, toothbrush],
        discount_percentage=20,
    )

    with pytest.raises(
        InvalidProductUnitError,
        match="Bundles can only be applied if every Product has ProductUnit.EACH, but Product\(name=apples\) has ProductUnit.KILO!",
    ):
        _create_discounts_from_bundles(
            product_quantities_map={apples: 2.5, toothbrush: 2},
            bundles=[bundle],
            catalog=catalog,
        )


def test_create_discounts(mocker):
    catalog = FakeCatalog()

    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=99)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=199)

    apples_offer = Offer(
        offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        product=apples,
        optional_argument=10,
    )

    melon = Product(name="melon", unit=ProductUnit.EACH)
    catalog.add_product(product=melon, price_cents=210)

    product_quantities_map = {toothbrush: 2, toothpaste: 3, apples: 4, melon: 2}
    product_offers_map = {apples: apples_offer}
    bundles = [bundle]

    mocked_create_discounts_from_offers = mocker.patch(
        "discount_creation._create_discounts_from_offers"
    )
    mocked_create_discounts_from_bundles = mocker.patch(
        "discount_creation._create_discounts_from_bundles"
    )

    create_discounts(
        product_quantities_map=product_quantities_map,
        product_offers_map=product_offers_map,
        bundles=bundles,
        catalog=catalog,
    )
    mocked_create_discounts_from_offers.assert_called_with(
        product_quantities_map=product_quantities_map,
        product_offers_map=product_offers_map,
        catalog=catalog,
    )
    mocked_create_discounts_from_bundles.assert_called_with(
        product_quantities_map=product_quantities_map,
        bundles=bundles,
        catalog=catalog,
    )
