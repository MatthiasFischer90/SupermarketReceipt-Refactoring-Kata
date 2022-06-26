import pytest

from model_objects import Product, ProductUnit
from shopping_cart import (
    IllegalQuantityForProductTypeError,
    ProductNotInCatalogError,
    ShoppingCart,
)
from tests.fake_catalog import FakeCatalog


def test_add_item_quantity():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    catalog.add_product(product=apples, price_cents=199)

    cart = ShoppingCart(catalog=catalog)
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
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    cart = ShoppingCart(catalog=catalog)
    with pytest.raises(
        IllegalQuantityForProductTypeError,
        match="Can't add 2.5 of Product\(name=toothbrush\) to cart - Products with ProductUnit.EACH must be added in integer quantities!",
    ):
        cart.add_item_quantity(product=toothbrush, quantity=2.5)


def test_fail_add_item_quantity_product_not_in_catalog():
    catalog = FakeCatalog()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    catalog.add_product(product=toothbrush, price_cents=100)

    apples = Product(name="apples", unit=ProductUnit.KILO)

    cart = ShoppingCart(catalog=catalog)
    with pytest.raises(
        ProductNotInCatalogError,
        match="Can't add Product\(name=apples\) to ShoppingCart - Product is not in Catalog that this ShoppingCart belongs to!",
    ):
        cart.add_item_quantity(product=apples, quantity=3.5)
