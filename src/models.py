from abc import ABC, abstractmethod


class LogMixin:
    """Миксин-класс для автоматического логирования создания объектов."""

    def __init__(self, name: str, description: str, price: float, quantity: int, *args, **kwargs) -> None:
        # Форматируем первые 4 базовых параметра строго в соответствии с ожиданиями тестов
        base_params = [name, description, price, quantity]
        all_params = ", ".join(repr(arg) for arg in base_params)
        print(f"Создан объект: {self.__class__.__name__}({all_params})")

        # Передаем управление дальше по MRO
        super().__init__(name=name, description=description, price=price, quantity=quantity, *args, **kwargs)


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех видов продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int, **kwargs) -> None:
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        super().__init__()


class Product(LogMixin, BaseProduct):
    """Класс для базового товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int, **kwargs):
        super().__init__(name, description, price, quantity, **kwargs)
        self.__price = price

    def __add__(self, other):
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только товары одного и того же класса")

    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Category:
    """Класс для категорий товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None) -> None:
        self.name = name
        self.description = description
        self.__products = []

        if products is not None:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total_quantity} шт.'

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Добавить можно только объект класса Product")

        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def average_price(self) -> float:
        try:
            total_price = sum(product.price for product in self.__products)
            avg_price = total_price / len(self.__products)
            return round(avg_price, 2)
        except ZeroDivisionError:
            return 0


class Smartphone(Product):
    """Класс для смартфонов."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str) -> None:
        super().__init__(
            name, description, price, quantity,
            efficiency=efficiency, model=model, memory=memory, color=color
        )
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str) -> None:
        super().__init__(
            name, description, price, quantity,
            country=country, germination_period=germination_period, color=color
        )
        self.country = country
        self.germination_period = germination_period
        self.color = color
