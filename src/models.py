class Product:
    """Класс для представления товара."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    # Атрибуты класса для подсчета количества категорий и уникальных товаров
    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []

        # Увеличиваем счетчик категорий при создании нового объекта
        Category.category_count += 1

    def add_product(self, product: Product):
        """Метод для добавления товара в категорию."""
        self.products.append(product)

        # Увеличиваем счетчик уникальных товаров при каждом добавлении в категорию
        Category.product_count += 1

