from approvaltests import verify

from model_objects import Product, ProductUnit, Discount
from receipt import Receipt
from receipt_printer import HtmlReceiptPrinter


def test_quantity_one():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    receipt.add_product(
        product=toothbrush, quantity=1, price_cents=99, total_price_cents=99
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))


def test_quantity_two():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    receipt.add_product(
        product=toothbrush, quantity=2, price_cents=99, total_price_cents=198
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))


def test_loose_weight():
    receipt = Receipt()
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(
        product=apples,
        quantity=2.3,
        price_cents=199,
        total_price_cents=round(199 * 2.3),
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))


def test_total():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(
        product=toothbrush, quantity=2, price_cents=99, total_price_cents=198
    )
    receipt.add_product(
        product=apples,
        quantity=0.75,
        price_cents=199,
        total_price_cents=round(199 * 0.75),
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))


def test_discounts():
    receipt = Receipt()
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_discounts(
        [Discount(product=apples, description="3 for 2", discount_amount_cents=-99)]
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))


def test_whole_receipt():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(
        product=toothbrush, quantity=3, price_cents=99, total_price_cents=297
    )
    receipt.add_product(
        product=apples,
        quantity=0.75,
        price_cents=199,
        total_price_cents=round(199 * 0.75),
    )
    receipt.add_discounts(
        [Discount(product=toothbrush, description="3 for 2", discount_amount_cents=-99)]
    )
    verify(HtmlReceiptPrinter().print_receipt(receipt=receipt))
