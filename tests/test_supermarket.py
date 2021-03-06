"""This module contains more comprehensive tests for different scenarios.

In the tests in this module, more complete test scenarios are covered that
in the test modules that contain unit tests. If this project was actually
connected to a database, this module's tests would most closely resemble
e2e tests that work with external resources.
"""

from model_objects import Bundle, Offer, Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_three_for_two_offer():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.THREE_FOR_TWO,
        product=toothbrush,
        optional_argument=None,
    )
    teller.add_offer(offer=offer)

    # test with only two toothbrushes
    cart_two_toothbrushes = ShoppingCart(catalog=catalog)
    cart_two_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_two_toothbrushes.add_item_quantity(product=toothbrush, quantity=2)
    receipt_two_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_two_toothbrushes
    )
    assert 800 == receipt_two_toothbrushes.get_total_price_cents()
    assert 0 == len(receipt_two_toothbrushes.discounts)

    # test with exactly three toothbrushes
    cart_three_toothbrushes = ShoppingCart(catalog=catalog)
    cart_three_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_three_toothbrushes.add_item_quantity(product=toothbrush, quantity=3)
    receipt_three_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_three_toothbrushes
    )
    assert 800 == receipt_three_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_three_toothbrushes.discounts)

    # test with eight toothbrushes
    cart_eight_toothbrushes = ShoppingCart(catalog=catalog)
    cart_eight_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_eight_toothbrushes.add_item_quantity(product=toothbrush, quantity=8)
    receipt_eight_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_eight_toothbrushes
    )
    assert 1200 == receipt_eight_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_eight_toothbrushes.discounts)


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=99)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=199)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.PERCENT_DISCOUNT,
        product=toothbrush,
        optional_argument=10.0,
    )
    teller.add_offer(offer=offer)

    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=apples, quantity=2.5)
    cart.add_item_quantity(product=toothbrush, quantity=2)

    receipt = teller.check_out_articles_from_cart(cart=cart)

    assert 676 == receipt.get_total_price_cents()
    assert 2 == len(receipt.items)

    # check apples
    receipt_item_apples = receipt.items[0]
    assert apples == receipt_item_apples.product
    assert 199 == receipt_item_apples.price_cents
    assert 498 == receipt_item_apples.total_price_cents
    assert 2.5 == receipt_item_apples.quantity

    # check toothbrushes
    receipt_item_toothbrush = receipt.items[1]
    assert toothbrush == receipt_item_toothbrush.product
    assert 99 == receipt_item_toothbrush.price_cents
    assert 198 == receipt_item_toothbrush.total_price_cents
    assert 2 == receipt_item_toothbrush.quantity


def test_two_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.TWO_FOR_AMOUNT,
        product=toothbrush,
        optional_argument=180,
    )
    teller.add_offer(offer=offer)

    # test with only one toothbrush
    cart_one_toothbrush = ShoppingCart(catalog=catalog)
    cart_one_toothbrush.add_item_quantity(product=apples, quantity=3)
    cart_one_toothbrush.add_item_quantity(product=toothbrush, quantity=1)
    receipt_one_toothbrush = teller.check_out_articles_from_cart(
        cart=cart_one_toothbrush
    )
    assert 700 == receipt_one_toothbrush.get_total_price_cents()
    assert 0 == len(receipt_one_toothbrush.discounts)

    # test with exactly two toothbrushes
    cart_two_toothbrushes = ShoppingCart(catalog=catalog)
    cart_two_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_two_toothbrushes.add_item_quantity(product=toothbrush, quantity=2)
    receipt_two_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_two_toothbrushes
    )
    assert 780 == receipt_two_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_two_toothbrushes.discounts)

    # test with five toothbrushes
    cart_five_toothbrushes = ShoppingCart(catalog=catalog)
    cart_five_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_five_toothbrushes.add_item_quantity(product=toothbrush, quantity=5)
    receipt_five_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_five_toothbrushes
    )
    assert 1060 == receipt_five_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_five_toothbrushes.discounts)


def test_five_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)
    offer = Offer(
        offer_type=SpecialOfferType.FIVE_FOR_AMOUNT,
        product=toothbrush,
        optional_argument=450,
    )
    teller.add_offer(offer=offer)

    # test with only one toothbrush
    cart_one_toothbrushes = ShoppingCart(catalog=catalog)
    cart_one_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_one_toothbrushes.add_item_quantity(product=toothbrush, quantity=1)
    receipt_one_toothbrush = teller.check_out_articles_from_cart(
        cart=cart_one_toothbrushes
    )
    assert 700 == receipt_one_toothbrush.get_total_price_cents()
    assert 0 == len(receipt_one_toothbrush.discounts)

    # test with exactly five toothbrushes
    cart_five_toothbrushes = ShoppingCart(catalog=catalog)
    cart_five_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_five_toothbrushes.add_item_quantity(product=toothbrush, quantity=5)
    receipt_five_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_five_toothbrushes
    )
    assert 1050 == receipt_five_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_five_toothbrushes.discounts)

    # test with 14 toothbrushes
    cart_fourteen_toothbrushes = ShoppingCart(catalog=catalog)
    cart_fourteen_toothbrushes.add_item_quantity(product=apples, quantity=3)
    cart_fourteen_toothbrushes.add_item_quantity(product=toothbrush, quantity=14)
    receipt_fourteen_toothbrushes = teller.check_out_articles_from_cart(
        cart=cart_fourteen_toothbrushes
    )
    assert 1900 == receipt_fourteen_toothbrushes.get_total_price_cents()
    assert 1 == len(receipt_fourteen_toothbrushes.discounts)


def test_price_can_be_zero_through_quantity():
    catalog = FakeCatalog()
    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=200)

    teller = Teller(catalog=catalog)

    # test with only 1 gram of apples
    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=apples, quantity=0.001)
    receipt = teller.check_out_articles_from_cart(cart=cart)
    assert 0 == receipt.get_total_price_cents()


def test_bundle():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
    catalog.add_product(product=toothpaste, price_cents=80)

    melon = Product(name="melon", unit=ProductUnit.EACH)
    catalog.add_product(product=melon, price_cents=210)

    teller = Teller(catalog=catalog)
    bundle = Bundle(
        products=[toothbrush, toothpaste],
        discount_percentage=20,
    )
    teller.add_bundle(bundle=bundle)

    # test with two toothbrushes and two toothpastes in bundle, and also 3 melons
    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=toothbrush, quantity=2)
    cart.add_item_quantity(product=toothpaste, quantity=2)
    cart.add_item_quantity(product=melon, quantity=3)
    receipt = teller.check_out_articles_from_cart(cart=cart)
    assert 918 == receipt.get_total_price_cents()
    assert 2 == len(receipt.discounts)

    # test with two toothbrushes and one toothpaste in bundle, and also 3 melons
    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=toothbrush, quantity=2)
    cart.add_item_quantity(product=toothpaste, quantity=1)
    cart.add_item_quantity(product=melon, quantity=3)
    receipt = teller.check_out_articles_from_cart(cart=cart)
    assert 874 == receipt.get_total_price_cents()
    assert 2 == len(receipt.discounts)

    # test with one toothbrush and without the toothpaste in bundle, and also 3 melons
    cart = ShoppingCart(catalog=catalog)
    cart.add_item_quantity(product=toothbrush, quantity=1)
    cart.add_item_quantity(product=melon, quantity=3)
    receipt = teller.check_out_articles_from_cart(cart=cart)
    assert 730 == receipt.get_total_price_cents()
    assert 0 == len(receipt.discounts)
