import pytest

from model_objects import Offer, Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_three_for_two_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog=catalog)
    # the passed "argument" in add_special_offer is not used anywhere, so value doesn't matter
    # TODO: Do something about comment above?
    offer = Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 1.0)
    teller.add_offer(offer=offer)

    # test with only two toothbrushes
    cart_two_toothbrushes = ShoppingCart()
    cart_two_toothbrushes.add_item_quantity(apples, 3)
    cart_two_toothbrushes.add_item_quantity(toothbrush, 2)
    receipt_two_toothbrushes = teller.check_out_articles_from_cart(
        cart_two_toothbrushes
    )
    assert 8 == receipt_two_toothbrushes.total_price()
    assert 0 == len(receipt_two_toothbrushes.discounts)

    # test with exactly three toothbrushes
    cart_three_toothbrushes = ShoppingCart()
    cart_three_toothbrushes.add_item_quantity(apples, 3)
    cart_three_toothbrushes.add_item_quantity(toothbrush, 3)
    receipt_three_toothbrushes = teller.check_out_articles_from_cart(
        cart_three_toothbrushes
    )
    assert 8 == receipt_three_toothbrushes.total_price()
    assert 1 == len(receipt_three_toothbrushes.discounts)

    # test with eight toothbrushes
    cart_eight_toothbrushes = ShoppingCart()
    cart_eight_toothbrushes.add_item_quantity(apples, 3)
    cart_eight_toothbrushes.add_item_quantity(toothbrush, 8)
    receipt_eight_toothbrushes = teller.check_out_articles_from_cart(
        cart_eight_toothbrushes
    )
    assert 12 == receipt_eight_toothbrushes.total_price()
    assert 1 == len(receipt_eight_toothbrushes.discounts)


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog=catalog)
    offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    teller.add_offer(offer=offer)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.check_out_articles_from_cart(cart)

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


def test_two_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog=catalog)
    offer = Offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.8)
    teller.add_offer(offer=offer)

    # test with only one toothbrush
    cart_one_toothbrush = ShoppingCart()
    cart_one_toothbrush.add_item_quantity(apples, 3)
    cart_one_toothbrush.add_item_quantity(toothbrush, 1)
    receipt_one_toothbrush = teller.check_out_articles_from_cart(cart_one_toothbrush)
    assert 7 == receipt_one_toothbrush.total_price()
    assert 0 == len(receipt_one_toothbrush.discounts)

    # test with exactly two toothbrushes
    cart_two_toothbrushes = ShoppingCart()
    cart_two_toothbrushes.add_item_quantity(apples, 3)
    cart_two_toothbrushes.add_item_quantity(toothbrush, 2)
    receipt_two_toothbrushes = teller.check_out_articles_from_cart(
        cart_two_toothbrushes
    )
    assert 7.8 == receipt_two_toothbrushes.total_price()
    assert 1 == len(receipt_two_toothbrushes.discounts)

    # test with five toothbrushes
    cart_five_toothbrushes = ShoppingCart()
    cart_five_toothbrushes.add_item_quantity(apples, 3)
    cart_five_toothbrushes.add_item_quantity(toothbrush, 5)
    receipt_five_toothbrushes = teller.check_out_articles_from_cart(
        cart_five_toothbrushes
    )
    assert 10.6 == receipt_five_toothbrushes.total_price()
    assert 1 == len(receipt_five_toothbrushes.discounts)


def test_five_for_amount_offer():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    teller = Teller(catalog=catalog)
    offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.5)
    teller.add_offer(offer=offer)

    # test with only one toothbrush
    cart_one_toothbrushes = ShoppingCart()
    cart_one_toothbrushes.add_item_quantity(apples, 3)
    cart_one_toothbrushes.add_item_quantity(toothbrush, 1)
    receipt_one_toothbrush = teller.check_out_articles_from_cart(cart_one_toothbrushes)
    assert 7 == receipt_one_toothbrush.total_price()
    assert 0 == len(receipt_one_toothbrush.discounts)

    # test with exactly five toothbrushes
    cart_five_toothbrushes = ShoppingCart()
    cart_five_toothbrushes.add_item_quantity(apples, 3)
    cart_five_toothbrushes.add_item_quantity(toothbrush, 5)
    receipt_five_toothbrushes = teller.check_out_articles_from_cart(
        cart_five_toothbrushes
    )
    assert 10.5 == receipt_five_toothbrushes.total_price()
    assert 1 == len(receipt_five_toothbrushes.discounts)

    # test with 14 toothbrushes
    cart_fourteen_toothbrushes = ShoppingCart()
    cart_fourteen_toothbrushes.add_item_quantity(apples, 3)
    cart_fourteen_toothbrushes.add_item_quantity(toothbrush, 14)
    receipt_fourteen_toothbrushes = teller.check_out_articles_from_cart(
        cart_fourteen_toothbrushes
    )
    assert 19 == receipt_fourteen_toothbrushes.total_price()
    assert 1 == len(receipt_fourteen_toothbrushes.discounts)


def test_fail_unexpected_special_offer_type():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    unexpected_special_offer_type = -500

    teller = Teller(catalog=catalog)
    offer = Offer(unexpected_special_offer_type, toothbrush, 3)
    teller.add_offer(offer=offer)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    with pytest.raises(ValueError):
        teller.check_out_articles_from_cart(cart)
