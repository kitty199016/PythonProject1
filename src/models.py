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

    # Атрибуты класса для подсчета количества категорий и товаров
    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list

    def __init__(self, name: str, description: str, products: list = None) -> None:
        self.name = name
        self.description = description

        # Если список товаров не передан, инициализируем его как пустой список
        self.products = products if products is not None else []

        # Увеличиваем счетчики при создании новой категории
        Category.category_count += 1
        Category.product_count += len(self.products)

    def add_product(self, product: Product):
        """Метод для добавления товара в категорию."""
        self.products.append(product)

        # Увеличиваем счетчик товаров при динамическом добавлении
        Category.product_count += 1

