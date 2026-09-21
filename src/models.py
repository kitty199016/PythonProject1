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
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество товаров: {total_quantity} шт.'

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию.
        Защищает список от добавления объектов, не являющихся Product или его наследниками.
        """
        # Проверяем, является ли объект экземпляром класса Product или его подклассов
        if not isinstance(product, Product):
            raise TypeError("Добавлять в категорию можно только товары (класса Product или его наследников)")

        # Логика проверки на уникальность по имени
        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        # Если продукт уникальный и валидный, добавляем его
        self.__products.append(product)
        Category.product_count += 1

    # Этот блок нужно оставить, а дубликат выше — удалить
    @property
    def products(self) -> str:
        """Возвращает строковое представление списка товаров."""
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
