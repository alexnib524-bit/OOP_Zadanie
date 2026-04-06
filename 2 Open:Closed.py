from dataclasses import dataclass
from abc import ABC, abstractmethod

#  Модели данных 
@dataclass
class Order:
    total: float


@dataclass
class Customer:
    kind: str


#  Стратегии скидок 
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, order: Order) -> float:
        pass


class RegularDiscount(DiscountStrategy):
    def apply(self, order: Order) -> float:
        return order.total


class VipDiscount(DiscountStrategy):
    def apply(self, order: Order) -> float:
        return order.total * 0.9


class EmployeeDiscount(DiscountStrategy):
    def apply(self, order: Order) -> float:
        return order.total * 0.8


class BlackFridayDiscount(DiscountStrategy):
    def apply(self, order: Order) -> float:
        return order.total * 0.5


#  Фабрика скидок 
class DiscountFactory:
    _strategies = {
        "regular": RegularDiscount,
        "vip": VipDiscount,
        "employee": EmployeeDiscount,
        "black_friday": BlackFridayDiscount,
    }
    
    @classmethod
    def get_strategy(cls, customer: Customer) -> DiscountStrategy:
        strategy_class = cls._strategies.get(customer.kind, RegularDiscount)
        return strategy_class()


# Центральный расчёт (не меняется при добавлении скидок) 
def apply_discount(order: Order, customer: Customer) -> float:
    strategy = DiscountFactory.get_strategy(customer)
    return strategy.apply(order)