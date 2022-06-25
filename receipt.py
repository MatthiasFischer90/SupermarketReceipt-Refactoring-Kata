from model_objects import Discount, Product


class ReceiptItem:
    def __init__(
        self, product: Product, quantity: float, price: float, total_price: float
    ):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    def total_price(self) -> float:
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discounts(self, discounts: list[Discount]) -> None:
        self._discounts += discounts

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
