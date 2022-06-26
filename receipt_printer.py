"""Module that contains the classes responsible for creating string representations of Receipts."""

from abc import ABC, abstractmethod

from model_objects import Discount, ProductUnit
from receipt import Receipt, ReceiptItem


class ReceiptPrinter(ABC):
    @abstractmethod
    def print_receipt(self, receipt: Receipt) -> str:
        """Creates a text representation of a given Receipt.

        Args:
            receipt (Receipt): The Receipt for which to create the text representation.

        Returns:
            str: The text representation of the given Receipt.
        """
        pass


class TextReceiptPrinter(ReceiptPrinter):
    """Class used to create text file representation of given Receipt.

    The resulting text representation is formatted similar to how the
    text would be formatted on a real-life receipt slip.
    """

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
        return result

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


class HtmlReceiptPrinter(ReceiptPrinter):
    """Class used to create HTML representation of given Receipt."""

    HTML_PREFIX = """<!DOCTYPE html>
<html>
  <head>
    <title>Receipt</title>
    <style>
      table, td, th { border : 1px solid black; }
      table { margin-bottom: 10px; margin-top: 10px;}
      th { padding : 13px; }
      td { padding : 15px; }
    </style>
  </head>
  <body>
    """

    HTML_SUFFIX = """  </body>
</html>"""

    def print_receipt(self, receipt: Receipt) -> str:
        body_indentation = 4
        result = self.HTML_PREFIX
        result += self._print_item_table(receipt=receipt, indentation=body_indentation)
        result += self._print_discount_table(
            receipt=receipt, indentation=body_indentation
        )
        result += self._print_total(receipt=receipt, indentation=body_indentation)
        result += self.HTML_SUFFIX
        return result

    def _print_indentation(self, indentation: int) -> str:
        return " " * indentation

    def _get_price_string(self, price_cents: int) -> str:
        return "%.2f" % (price_cents / 100)

    def _get_quantity_string(self, item: ReceiptItem) -> str:
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return "%.3f" % item.quantity

    def _print_item_table(self, receipt: Receipt, indentation: int) -> str:
        if len(receipt.items) == 0:
            return ""

        content = "<table>\n"
        content += self._print_item_table_headers(indentation=(indentation + 2))
        for item in receipt.items:
            content += self._print_item_table_row(
                item=item, indentation=(indentation + 2)
            )
        content += self._print_indentation(indentation=indentation)
        content += "</table>\n"
        return content

    def _print_item_table_headers(self, indentation: int) -> str:
        result = self._print_indentation(indentation=indentation)
        result += "<tr>\n"
        result += self._print_indentation(indentation=(indentation + 2))
        result += "<th>Product name</th>\n"
        result += self._print_indentation(indentation=(indentation + 2))
        result += "<th>Unit price (EUR)</th>\n"
        result += self._print_indentation(indentation=(indentation + 2))
        result += "<th>Quantity</th>\n"
        result += self._print_indentation(indentation=(indentation + 2))
        result += "<th>Total price (EUR)</th>\n"
        result += self._print_indentation(indentation=indentation)
        result += "</tr>\n"
        return result

    def _print_item_table_row(self, item: ReceiptItem, indentation: int) -> str:
        row = self._print_indentation(indentation=indentation)
        row += "<tr>\n"
        row += self._print_product_name(item=item, indentation=(indentation + 2))
        row += self._print_item_unit_price(item=item, indentation=(indentation + 2))
        row += self._print_item_quantity(item=item, indentation=(indentation + 2))
        row += self._print_item_total_price(item=item, indentation=(indentation + 2))
        row += self._print_indentation(indentation=indentation)
        row += "</tr>\n"
        return row

    def _print_product_name(self, item: ReceiptItem, indentation: int) -> str:
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{item.product.name}</td>\n"
        return cell

    def _print_item_unit_price(self, item: ReceiptItem, indentation: int) -> str:
        price_euros_string = self._get_price_string(price_cents=item.price_cents)
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{price_euros_string}</td>\n"
        return cell

    def _print_item_quantity(self, item: ReceiptItem, indentation: int) -> str:
        quantity_string = self._get_quantity_string(item=item)
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{quantity_string}</td>\n"
        return cell

    def _print_item_total_price(self, item: ReceiptItem, indentation: int) -> str:
        price_euros_string = self._get_price_string(price_cents=item.total_price_cents)
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{price_euros_string}</td>\n"
        return cell

    def _print_discount_table(self, receipt: Receipt, indentation: int) -> str:
        if len(receipt.discounts) == 0:
            return ""

        content = self._print_indentation(indentation=indentation)
        content += "<table>\n"
        content += self._print_discount_table_headers(indentation=(indentation + 2))
        for discount in receipt.discounts:
            content += self._print_discount_table_row(
                discount=discount, indentation=(indentation + 2)
            )
        content += self._print_indentation(indentation=indentation)
        content += "</table>\n"
        return content

    def _print_discount_table_headers(self, indentation: int) -> str:
        row = self._print_indentation(indentation=indentation)
        row += "<tr>\n"
        row += self._print_indentation(indentation=(indentation + 2))
        row += "<th>Discount description</th>\n"
        row += self._print_indentation(indentation=(indentation + 2))
        row += "<th>Discount value (EUR)</th>\n"
        row += self._print_indentation(indentation=indentation)
        row += "</tr>\n"
        return row

    def _print_discount_table_row(self, discount: Discount, indentation: int) -> str:
        row = self._print_indentation(indentation=indentation)
        row += "<tr>\n"
        row += self._print_discount_description(
            discount=discount, indentation=(indentation + 2)
        )
        row += self._print_discount_value(
            discount=discount, indentation=(indentation + 2)
        )
        row += self._print_indentation(indentation=indentation)
        row += "</tr>\n"
        return row

    def _print_discount_description(self, discount: Discount, indentation: int) -> str:
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{discount.description}</td>\n"
        return cell

    def _print_discount_value(self, discount: Discount, indentation: int) -> str:
        discount_value_euros_string = self._get_price_string(
            price_cents=discount.discount_amount_cents
        )
        cell = self._print_indentation(indentation=indentation)
        cell += f"<td>{discount_value_euros_string}</td>\n"
        return cell

    def _print_total(self, receipt: Receipt, indentation: int) -> str:
        total_price_euros_string = self._get_price_string(
            price_cents=receipt.get_total_price_cents()
        )
        line = self._print_indentation(indentation=indentation)
        line += f"<p>Total: {total_price_euros_string}</p>\n"
        return line
