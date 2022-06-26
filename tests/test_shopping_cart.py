import pytest

from model_objects import Product, ProductUnit
from shopping_cart import ShoppingCart


def test_add_item_quantity():
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    apples = Product(name="apples", unit=ProductUnit.KILO)

    cart = ShoppingCart()
    cart.add_item_quantity(product=toothbrush, quantity=3)
    cart.add_item_quantity(product=apples, quantity=2.5)

    assert {
        toothbrush: 3,
        apples: 2.5,
    } == cart._product_quantities

    cart.add_item_quantity(product=apples, quantity=1.2)
    assert {
        toothbrush: 3,
        apples: 3.7,
    } == cart._product_quantities


def test_fail_add_item_quantity_unexpected_float_quantity():
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)

    cart = ShoppingCart()
    with pytest.raises(
        ValueError,
        match="Can't add 2.5 of toothbrush to cart - Products with ProductUnit.EACH must be added in integer quantities!",
    ):
        cart.add_item_quantity(product=toothbrush, quantity=2.5)
