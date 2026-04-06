from abc import ABC, abstractmethod

# Маленькие интерфейсы (принцип разделения интерфейса)

class Printable(ABC):
    @abstractmethod
    def print(self, text: str) -> None:
        pass


class Scannable(ABC):
    @abstractmethod
    def scan(self) -> str:
        pass


class Faxable(ABC):
    @abstractmethod
    def fax(self, number: str) -> None:
        pass


class Copiable(ABC):
    @abstractmethod
    def copy(self) -> None:
        pass


# Реализации (только нужные методы) 

class SimplePrinter(Printable):
    """Простой принтер - только печать"""
    
    def print(self, text: str) -> None:
        print(text)


class MultiFunctionMachine(Printable, Scannable, Faxable, Copiable):
    """Многофункциональное устройство - все функции"""
    
    def print(self, text: str) -> None:
        print(f"Printing: {text}")
    
    def scan(self) -> str:
        return "Scanned content"
    
    def fax(self, number: str) -> None:
        print(f"Faxing to {number}")
    
    def copy(self) -> None:
        print("Copying")


# Клиентский код (зависит только от нужного интерфейса) 

def print_document(printer: Printable, text: str) -> None:
    """Функция зависит только от Printable, не знает о scan/fax/copy"""
    printer.print(text)