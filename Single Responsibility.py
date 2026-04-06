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


# Загрузка 
class OrderLoader:
    
    
    def load(self, json_path: str) -> List[dict]:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)


# Валидация и парсинг 
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


# Форматирование 
class ReportFormatter:
    
    
    def format(self, orders: List[Order], total: float) -> str:
        return f"Orders count: {len(orders)}\nTotal: {total:.2f}\n"


#  Отправка (можно отключить/заменить) 
class EmailSender(ABC):
    
    
    @abstractmethod
    def send_report(self, orders: List[Order], report: str) -> None:
        pass


class RealEmailSender(EmailSender):
    
    
    def send_report(self, orders: List[Order], report: str) -> None:
        for o in orders:
            self._send_email(o.customer_email, "Your order report", report)
    
    def _send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[EMAIL to={to}] {subject}\n{body}")


class DisabledEmailSender(EmailSender):
    
    
    def send_report(self, orders: List[Order], report: str) -> None:
        pass  


# Главный сервис (оркестратор) 
class OrderReportService:
   
    
    def __init__(self, sender: EmailSender = None):
        self.loader = OrderLoader()
        self.parser = OrderParser()
        self.calculator = OrderCalculator()
        self.formatter = ReportFormatter()
        self.sender = sender if sender else RealEmailSender()
    
    def make_and_send_report(self, json_path: str) -> str:
        #  Загрузка
        raw_data = self.loader.load(json_path)
        
        #  Валидация + парсинг
        orders = self.parser.parse(raw_data)
        
        #  Расчёт
        total = self.calculator.calculate_total(orders)
        
        #  Форматирование
        report = self.formatter.format(orders, total)
        
        #  Отправка
        self.sender.send_report(orders, report)
        
        return report


#  Демонстрация работы 
if __name__ == "__main__":
    
    try:
        with open("orders.json", "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        sample_data = [
            {"id": "1", "price": 10.5, "qty": 2, "email": "test@example.com"},
            {"id": "2", "price": 20.0, "qty": 1, "email": "test2@example.com"}
        ]
        with open("orders.json", "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2)
        print(" Создан файл orders.json с тестовыми данными\n")
    
    print("=" * 50)
    print("1. СТАНДАРТНАЯ РАБОТА (с отправкой email)")
    print("=" * 50)
    service = OrderReportService()
    result = service.make_and_send_report("orders.json")
    print(f"\nОтчёт:\n{result}")
    
    print("\n" + "=" * 50)
    print("2. ОТПРАВКА ОТКЛЮЧЕНА (без правок форматирования/загрузки)")
    print("=" * 50)
    service_no_send = OrderReportService(sender=DisabledEmailSender())
    result = service_no_send.make_and_send_report("orders.json")
    print(f"Отчёт создан, но email не отправлен:\n{result}")
    
    print("\n" + "=" * 50)
    print("3. НОВЫЙ ФОРМАТ ОТЧЁТА (без правок в расчёте)")
    print("=" * 50)
    
    
    class NewFormatFormatter(ReportFormatter):
        def format(self, orders: List[Order], total: float) -> str:
            return f"=== REPORT ===\nOrders: {len(orders)}\nTotal sum: ${total:.2f}\n=============="
    
    service_new_format = OrderReportService()
    service_new_format.formatter = NewFormatFormatter()
    result = service_new_format.make_and_send_report("orders.json")
    print(f"\nОтчёт в новом формате:\n{result}")