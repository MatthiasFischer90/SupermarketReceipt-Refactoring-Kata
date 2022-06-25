from approvaltests import verify

from model_objects import Product, ProductUnit, Discount
from receipt import Receipt
from receipt_printer import ReceiptPrinter


def test_one_line_item():
    receipt = Receipt()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_quantity_two():
    receipt = Receipt()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    receipt.add_product(toothbrush, 2, 0.99, 0.99 * 2)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_loose_weight():
    receipt = Receipt()
    apples = Product("apples", ProductUnit.KILO)
    receipt.add_product(apples, 2.3, 1.99, 1.99 * 2.3)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_total():
    receipt = Receipt()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    receipt.add_product(toothbrush, 1, 0.99, 0.99 * 2)
    receipt.add_product(apples, 0.75, 1.99, 1.99 * 0.75)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_discounts():
    receipt = Receipt()
    apples = Product("apples", ProductUnit.KILO)
    receipt.add_discount(Discount(apples, "3 for 2", -0.99))
    verify(ReceiptPrinter().print_receipt(receipt))


def test_whole_receipt():
    receipt = Receipt()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)
    receipt.add_product(toothbrush, 2, 0.99, 0.99 * 2)
    receipt.add_product(apples, 0.75, 1.99, 1.99 * 0.75)
    receipt.add_discount(Discount(apples, "3 for 2", -0.99))
    verify(ReceiptPrinter().print_receipt(receipt))
