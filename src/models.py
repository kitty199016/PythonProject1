class Product:
    """Класс для представления товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    def __add__(self, other):
        """
        Возвращает суммарную стоимость двух товаров.
        Складывать можно только объекты абсолютно одинаковых классов.
        """
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только товары одного и того же класса")


    def __str__(self):
        # Реализовано строковое отображение в заданном формате
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    @classmethod
    def new_product(cls, product_data: dict):
        """Метод-фабрика для создания объекта Product из словаря."""
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
            print("Цена не должна быть нулевая или отрицательная")
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
        # Количество продуктов считается как сумма всех единиц товара на складе (quantity)
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total_quantity} шт.'

    def add_product(self, product: Product) -> None:
        """Метод для добавления товара Product в приватный список товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Оптимизированный геттер для вывода списка товаров с использованием str(product)."""
        # Преобразуем каждый объект продукта в строку благодаря реализованному Product.__str__
        return "\n".join(str(product) for product in self.__products)


class Smartphone(Product):
    """Класс для представления смартфона, наследуется от Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str) -> None:
        # Инициализируем свойства родительского класса Product
        super().__init__(name, description, price, quantity)

        # Добавляем новые специфичные свойства смартфона
        self.efficiency = efficiency  # Производительность
        self.model = model  # Модель
        self.memory = memory  # Объем встроенной памяти (ГБ)
        self.color = color  # Цвет


class LawnGrass(Product):
    """Класс для представления газонной травы, наследуется от Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str) -> None:
        # Инициализируем свойства родительского класса Product
        super().__init__(name, description, price, quantity)

        # Добавляем новые специфичные свойства газонной травы
        self.country = country  # Страна-производитель
        self.germination_period = germination_period  # Срок прорастания (в днях)
        self.color = color  # Цвет
