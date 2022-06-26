from unittest.mock import ANY, call
import pytest
from receipt import Receipt
from shopping_cart import ShoppingCart
from tests.fake_catalog import FakeCatalog
from model_objects import Bundle, Offer, Product, ProductUnit, SpecialOfferType
from teller import Teller, AlreadyHasBundleError, AlreadyHasOfferError


def test_fail_add_offer_with_existing_offer():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    teller = Teller(catalog=catalog)
    offer_one = Offer(
        offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        product=toothbrush,
        optional_argument=20,
    )
    teller.add_offer(offer=offer_one)
    offer_two = Offer(
        offer_type=SpecialOfferType.FIVE_FOR_AMOUNT,
        product=toothbrush,
        optional_argument=400,
    )
    with pytest.raises(
        AlreadyHasOfferError,
        match="Can't add Offer for Product\(name=toothbrush\): Product already has an Offer!",
    ):
        teller.add_offer(offer=offer_two)


def test_fail_add_offer_with_existing_bundle():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    teller = Teller(catalog=catalog)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    teller.add_bundle(bundle=bundle)
    offer = Offer(
        offer_type=SpecialOfferType.FIVE_FOR_AMOUNT,
        product=toothbrush,
        optional_argument=400,
    )
    with pytest.raises(
        AlreadyHasBundleError,
        match="Can't add Offer for Product\(name=toothbrush\): Product already has a Bundle!",
    ):
        teller.add_offer(offer=offer)


def test_fail_add_bundle_with_existing_offer():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        product=toothbrush,
        optional_argument=20,
    )
    teller.add_offer(offer=offer)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=10,
    )
    with pytest.raises(
        AlreadyHasOfferError,
        match="Can't add Bundle for Product\(name=toothbrush\): Product already has an Offer!",
    ):
        teller.add_bundle(bundle=bundle)


def test_fail_add_bundle_with_existing_bundle():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    dental_floss = Product(name="dental floss", unit=ProductUnit.EACH)
    catalog.add_product(product=dental_floss, price_cents=60)

    teller = Teller(catalog=catalog)
    bundle_one = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    teller.add_bundle(bundle=bundle_one)
    bundle_two = Bundle(
        products=[toothbrush, dental_floss],
        discount_percentage=10,
    )
    with pytest.raises(
        AlreadyHasBundleError,
        match="Can't add Bundle for Product\(name=toothbrush\): Product already has a Bundle!",
    ):
        teller.add_bundle(bundle=bundle_two)


def test_add_products_to_receipt(mocker):
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.THREE_FOR_TWO,
        product=apples,
        optional_argument=None,
    )
    teller.add_offer(offer=offer)

    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=toothbrush, quantity=2)
    cart.add_item_quantity(product=apples, quantity=3.017)

    receipt = Receipt()

    add_product_spy = mocker.spy(receipt, "add_product")
    teller._add_products_to_receipt(
        receipt=receipt, product_quantities=cart.product_quantities
    )
    expected_calls = [
        call(
            product=toothbrush,
            quantity=2,
            price_cents=100,
            total_price_cents=200,
        ),
        call(
            product=apples,
            quantity=3.017,
            price_cents=200,
            total_price_cents=603,
        ),
    ]
    assert expected_calls == add_product_spy.call_args_list


def test_check_out_articles_from_cart(mocker):
    mocked_add_products_to_receipt = mocker.patch(
        "teller.Teller._add_products_to_receipt"
    )
    mocked_create_discounts = mocker.patch("teller.create_discounts")

    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.THREE_FOR_TWO,
        product=apples,
        optional_argument=None,
    )
    teller.add_offer(offer=offer)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    teller.add_bundle(bundle=bundle)

    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=apples, quantity=3.5)
    cart.add_item_quantity(product=toothbrush, quantity=2)
    cart.add_item_quantity(product=toothpaste, quantity=3)
    teller.check_out_articles_from_cart(cart=cart)

    expected_product_quantities_map = {
        apples: 3.5,
        toothbrush: 2,
        toothpaste: 3,
    }
    mocked_add_products_to_receipt.assert_called_with(
        receipt=ANY,
        product_quantities=expected_product_quantities_map,
    )
    expected_product_offers_map = {apples: offer}
    mocked_create_discounts.assert_called_with(
        product_quantities_map=expected_product_quantities_map,
        product_offers_map=expected_product_offers_map,
        bundles=[bundle],
        catalog=catalog,
    )
