import json
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

# Модель данных 
@dataclass
class Order:
    id: str
    price: float
    qty: int
    customer_email: str


#  Загрузка 
class OrderLoader:
    def load(self, json_path: str) -> List[dict]:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)


#  Валидация и парсинг 
class OrderParser:
    def parse(self, raw_data: List[dict]) -> List[Order]:
        orders = []
        for item in raw_data:
            self._validate(item)
            orders.append(self._to_order(item))
        return orders
    
    def _validate(self, item: dict) -> None:
        if "id" not in item or "price" not in item or "qty" not in item or "email" not in item:
            raise ValueError("Invalid order payload")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")
    
    def _to_order(self, item: dict) -> Order:
        return Order(
            item["id"],
            float(item["price"]),
            int(item["qty"]),
            item["email"]
        )


#  Расчёт 
class OrderCalculator:
    def calculate_total(self, orders: List[Order]) -> float:
        return sum(o.price * o.qty for o in orders)


#  Форматирование 
class ReportFormatter:
    def format(self, orders: List[Order], total: float) -> str:
        return f"Orders count: {len(orders)}\nTotal: {total:.2f}\n"


#  Отправка 
class ReportSender(ABC):
    @abstractmethod
    def send(self, orders: List[Order], report: str) -> None:
        pass


class EmailSender(ReportSender):
    def send(self, orders: List[Order], report: str) -> None:
        for o in orders:
            self._send_email(o.customer_email, "Your order report", report)
    
    def _send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[EMAIL to={to}] {subject}\n{body}")


class DisabledSender(ReportSender):
    def send(self, orders: List[Order], report: str) -> None:
        pass


#  Главный сервис 
class OrderReportService:
    def __init__(self, loader: OrderLoader = None, parser: OrderParser = None, 
                 calculator: OrderCalculator = None, formatter: ReportFormatter = None,
                 sender: ReportSender = None):
        self.loader = loader or OrderLoader()
        self.parser = parser or OrderParser()
        self.calculator = calculator or OrderCalculator()
        self.formatter = formatter or ReportFormatter()
        self.sender = sender or EmailSender()
    
    def make_and_send_report(self, json_path: str) -> str:
        raw_data = self.loader.load(json_path)
        orders = self.parser.parse(raw_data)
        total = self.calculator.calculate_total(orders)
        report = self.formatter.format(orders, total)
        self.sender.send(orders, report)
        return report