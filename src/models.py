from abc import ABC, abstractmethod


class LogMixin:
    """Класс-миксин для автоматического логирования создания объектов."""

    def __init__(self, *args, **kwargs) -> None:
        # Инициализируем свойства следующих классов в цепочке MRO (BaseProduct)
        super().__init__(*args, **kwargs)

        # Собираем позиционные аргументы (например, имя, описание, цена, количество)
        args_str = ", ".join(repr(arg) for arg in args)
        # Собираем именованные аргументы, если они передавались
        kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())

        # Объединяем параметры в одну строку для вывода
        all_params = ", ".join(filter(None, [args_str, kwargs_str]))

        # Выводим имя фактического класса, который создается в данный момент
        print(f"Создан объект: {self.__class__.__name__}({all_params})")


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех типов продуктов магазина."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Каждый продукт должен иметь имя, описание, цену и количество."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Каждый продукт должен предоставлять строковое представление."""
        pass

    @abstractmethod
    def __add__(self, other):
        """Каждый продукт должен поддерживать операцию сложения стоимости."""
        pass


# Добавляем LogMixin первым в цепочку наследования Product
class Product(LogMixin, BaseProduct):
    """Класс для представления товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Вызываем конструктор цепочки MRO. Первым отработает LogMixin, затем BaseProduct
        super().__init__(name, description, price, quantity)
        self.__price = price  # Приватный атрибут цены

    def __add__(self, other):
        """
        Возвращает суммарную стоимость двух товаров.
        Складывать можно только объекты абсолютно одинаковых классов.
        """
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только товары одного и того же класса")

    def __str__(self):
        # Строковое представление товара
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    @classmethod
    def new_product(cls, product_data: dict):
        """Класс-метод для создания объекта Product из словаря."""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )

    @property
    def price(self) -> float:
        """Геттер для получения цены товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для изменения цены товара с валидацией."""
        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной")
        else:
            self.__price = new_price


class Category:
    """Класс для представления категории товаров."""

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
        """Добавляет продукт в категорию с валидацией типа."""
        if not isinstance(product, Product):
            raise TypeError("Добавлять в категорию можно только товары (класса Product или его наследников)")

        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строковое представление списка товаров."""
        return "\n".join(str(product) for product in self.__products)


class Smartphone(Product):
    """Класс для представления смартфона, наследуется от Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str) -> None:
        super().__init__(name, description, price, quantity)

        # Специфичные свойства смартфона
        self.efficiency = efficiency  # Производительность
        self.model = model  # Модель
        self.memory = memory  # Объем встроенной памяти (ГБ)
        self.color = color  # Цвет


class LawnGrass(Product):
    """Класс для представления газонной травы, наследуется от Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str) -> None:
        super().__init__(name, description, price, quantity)

        # Специфичные свойства газонной травы
        self.country = country  # Страна-производитель
        self.germination_period = germination_period  # Срок прорастания (в днях)
        self.color = color  # Цвет
