from typing import Union
from model_objects import Discount, Product


class ReceiptItem:
    def __init__(
        self,
        product: Product,
        quantity: Union[int, float],
        price_cents: int,
        total_price_cents: int,
    ):
        self.product = product
        self.quantity = quantity
        self.price_cents = price_cents
        self.total_price_cents = total_price_cents


class Receipt:
    def __init__(self):
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    def get_total_price_cents(self) -> int:
        total = 0
        for item in self.items:
            total += item.total_price_cents
        for discount in self.discounts:
            total += discount.discount_amount_cents
        return total

    def add_product(
        self,
        product: Product,
        quantity: Union[int, float],
        price_cents: int,
        total_price_cents: int,
    ) -> None:
        self._items.append(
            ReceiptItem(
                product=product,
                quantity=quantity,
                price_cents=price_cents,
                total_price_cents=total_price_cents,
            )
        )

    def add_discounts(self, discounts: list[Discount]) -> None:
        self._discounts += discounts

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
