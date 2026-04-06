from abc import ABC, abstractmethod
from dataclasses import dataclass

# Абстрактный класс для всех фигур 
class Shape(ABC):
    @abstractmethod
    def area(self) -> int:
        pass


#  Прямоугольник (независимый класс, не предок квадрата) 
@dataclass
class Rectangle(Shape):
    width: int
    height: int
    
    def area(self) -> int:
        return self.width * self.height


# Квадрат (отдельный класс, не наследник Rectangle) 
@dataclass
class Square(Shape):
    side: int
    
    def area(self) -> int:
        return self.side * self.side


#  Функция, которая работает с любой фигурой 
def resize_and_get_area(shape: Shape, new_width: int, new_height: int) -> int:
    if isinstance(shape, Rectangle):
        shape.width = new_width
        shape.height = new_height
    elif isinstance(shape, Square):
        shape.side = min(new_width, new_height)
    return shape.area()