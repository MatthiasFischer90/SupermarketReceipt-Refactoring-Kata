import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 6.75 == pytest.approx(receipt.total_price(), 0.01)
    assert 2 == len(receipt.items)

    # check apples
    receipt_item_apples = receipt.items[0]
    assert apples == receipt_item_apples.product
    assert 1.99 == receipt_item_apples.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item_apples.total_price, 0.01)
    assert 2.5 == receipt_item_apples.quantity

    # check toothbrushes
    receipt_item_toothbrush = receipt.items[1]
    assert toothbrush == receipt_item_toothbrush.product
    assert 0.99 == receipt_item_toothbrush.price
    assert 2 * 0.99 == pytest.approx(receipt_item_toothbrush.total_price, 0.01)
    assert 2 == receipt_item_toothbrush.quantity


def test_three_for_two_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    # test with exactly three toothbrushes
    cart_one = ShoppingCart()
    cart_one.add_item_quantity(apples, 3)
    cart_one.add_item_quantity(toothbrush, 3)
    receipt_one = teller.checks_out_articles_from(cart_one)
    assert 8 == receipt_one.total_price()
    assert 1 == len(receipt_one.discounts)

    # test with eight toothbrushes
    cart_two = ShoppingCart()
    cart_two.add_item_quantity(apples, 3)
    cart_two.add_item_quantity(toothbrush, 8)
    receipt_two = teller.checks_out_articles_from(cart_two)
    assert 12 == receipt_two.total_price()
    assert 1 == len(receipt_two.discounts)


def test_two_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.8)

    # test with exactly two toothbrushes
    cart_one = ShoppingCart()
    cart_one.add_item_quantity(apples, 3)
    cart_one.add_item_quantity(toothbrush, 2)
    receipt_one = teller.checks_out_articles_from(cart_one)
    assert 7.8 == receipt_one.total_price()
    assert 1 == len(receipt_one.discounts)

    # test with five toothbrushes
    cart_two = ShoppingCart()
    cart_two.add_item_quantity(apples, 3)
    cart_two.add_item_quantity(toothbrush, 5)
    receipt_two = teller.checks_out_articles_from(cart_two)
    assert 10.6 == receipt_two.total_price()
    assert 1 == len(receipt_two.discounts)


def test_five_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.5)

    # test with exactly five toothbrushes
    cart_one = ShoppingCart()
    cart_one.add_item_quantity(apples, 3)
    cart_one.add_item_quantity(toothbrush, 5)
    receipt_one = teller.checks_out_articles_from(cart_one)
    assert 10.5 == receipt_one.total_price()
    assert 1 == len(receipt_one.discounts)

    # test with 14 toothbrushes
    cart_two = ShoppingCart()
    cart_two.add_item_quantity(apples, 3)
    cart_two.add_item_quantity(toothbrush, 14)
    receipt_two = teller.checks_out_articles_from(cart_two)
    assert 19 == receipt_two.total_price()
    assert 1 == len(receipt_two.discounts)
