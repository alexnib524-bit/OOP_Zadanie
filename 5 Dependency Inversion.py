from abc import ABC, abstractmethod
from typing import List

# Абстракция уведомления 

class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, text: str) -> None:
        pass


# Конкретные реализации 

class EmailNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[EMAIL to={to}] {text}")


class SmsNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[SMS to={to}] {text}")


class PushNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[PUSH to={to}] {text}")


class FakeNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        pass


# Сервис уведомлений с внедрением зависимостей 

class NotificationService:
    def __init__(self, notifiers: List[Notifier]):
        self.notifiers = notifiers
    
    def notify(self, text: str, recipients: List[tuple]) -> None:
        """
        recipients: список пар (получатель, notifier_index)
        например: [("user@mail.com", 0), ("+79123456789", 1)]
        """
        for to, notifier in recipients:
            self.notifiers[notifier].send(to, text)