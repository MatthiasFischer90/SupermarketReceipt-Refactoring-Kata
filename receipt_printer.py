from model_objects import Discount, ProductUnit

from receipt import Receipt, ReceiptItem


class ReceiptPrinter:
    def __init__(self, columns: int = 40):
        if columns < 1:
            raise ValueError(f"columns must be positive integer, but got {columns}!")
        self.columns = columns

    def print_receipt(self, receipt: Receipt) -> str:
        result = ""
        for item in receipt.items:
            receipt_item = self._print_receipt_item(item=item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self._print_discount(discount=discount)
            result += discount_presentation

        result += "\n"
        result += self._present_total(receipt=receipt)
        return str(result)

    def _print_receipt_item(self, item: ReceiptItem) -> str:
        total_price_printed = self._print_price(price_cents=item.total_price_cents)
        name = item.product.name
        line = self._format_line_with_whitespace(name=name, value=total_price_printed)
        if item.quantity != 1:
            line += f"  {self._print_price(price_cents=item.price_cents)} * {self._print_quantity(item=item)}\n"
        return line

    def _format_line_with_whitespace(self, name: str, value: str) -> str:
        line = name
        # leave at least one whitespace between name and value
        line += " "
        whitespace_size = self.columns - len(line) - len(value)
        for _ in range(whitespace_size):
            line += " "
        line += value
        line += "\n"
        return line

    def _print_price(self, price_cents: int) -> str:
        return "%.2f" % (price_cents / 100)

    def _print_quantity(self, item: ReceiptItem) -> str:
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return "%.3f" % item.quantity

    def _print_discount(self, discount: Discount) -> str:
        name = f"{discount.description} ({discount.product.name})"
        value = self._print_price(price_cents=discount.discount_amount_cents)
        return self._format_line_with_whitespace(name=name, value=value)

    def _present_total(self, receipt: Receipt) -> str:
        name = "Total: "
        value = self._print_price(price_cents=receipt.get_total_price_cents())
        return self._format_line_with_whitespace(name=name, value=value)
