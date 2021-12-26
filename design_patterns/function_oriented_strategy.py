from typing import Callable, NamedTuple, Optional, Sequence
from decimal import Decimal
from dataclasses import dataclass


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal
    
    def total(self):
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable] = None
    
    def total(self):
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))
    
    def due(self):
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


def fidelity_promo(order):
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order):
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)


if __name__ == "__main__":
    joe = Customer('John Doe', 0)
    cart = [LineItem('banana', 4, Decimal('.5')),
            LineItem('apple', 10, Decimal('1.5')),
            LineItem('watermelon', 5, Decimal(5))]
    order = Order(joe, cart, fidelity_promo)
    print(order)