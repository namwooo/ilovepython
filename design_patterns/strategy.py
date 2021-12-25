from abc import ABC, abstractmethod
from typing import NamedTuple, Optional, Sequence
from decimal import Decimal


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal
    
    def total(self):
        return self.price * self.quantity


class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional['Promotion'] = None
    
    def total(self):
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))
    
    def due(self):
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    
    
class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount."""


class FidelityPromo(Promotion):
    def discount(self, order):
        rate = Decimal('0.05')
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromo(Promotion):
    def discount(self, order):
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount
    

class LargeOrderPromo(Promotion):
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)
    