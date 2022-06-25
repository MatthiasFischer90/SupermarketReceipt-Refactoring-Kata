from approvaltests import verify

from model_objects import Product, ProductUnit, Discount
from receipt import Receipt
from receipt_printer import ReceiptPrinter


def test_one_line_item():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    receipt.add_product(product=toothbrush, quantity=1, price=0.99, total_price=0.99)
    verify(ReceiptPrinter().print_receipt(receipt=receipt))


def test_quantity_two():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    receipt.add_product(
        product=toothbrush, quantity=2, price=0.99, total_price=0.99 * 2
    )
    verify(ReceiptPrinter().print_receipt(receipt=receipt))


def test_loose_weight():
    receipt = Receipt()
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(
        product=apples, quantity=2.3, price=1.99, total_price=1.99 * 2.3
    )
    verify(ReceiptPrinter().print_receipt(receipt=receipt))


def test_total():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(
        product=toothbrush, quantity=1, price=0.99, total_price=0.99 * 2
    )
    receipt.add_product(
        product=apples, quantity=0.75, price=1.99, total_price=1.99 * 0.75
    )
    verify(ReceiptPrinter().print_receipt(receipt=receipt))


def test_discounts():
    receipt = Receipt()
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_discounts([Discount(apples, "3 for 2", -0.99)])
    verify(ReceiptPrinter().print_receipt(receipt=receipt))


def test_whole_receipt():
    receipt = Receipt()
    toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
    apples = Product(name="apples", unit=ProductUnit.KILO)
    receipt.add_product(product=toothbrush, quantity=1, price=0.99, total_price=0.99)
    receipt.add_product(
        product=toothbrush, quantity=2, price=0.99, total_price=0.99 * 2
    )
    receipt.add_product(
        product=apples, quantity=0.75, price=1.99, total_price=1.99 * 0.75
    )
    receipt.add_discounts([Discount(apples, "3 for 2", -0.99)])
    verify(ReceiptPrinter().print_receipt(receipt=receipt))
