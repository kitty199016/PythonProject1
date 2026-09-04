class Product:
    """Класс для представления товара."""

    # Атрибуты класса (счетчик общего количества уникальных продуктов)
    product_count = 0

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

        # Увеличиваем счетчик при создании каждого нового продукта
        Product.product_count += 1


class Category:
    """Класс для представления категории товаров."""

    # Атрибуты класса (счетчик общего количества категорий)
    category_count = 0

    name: str
    description: str
    products: list

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []  # Список товаров изначально пустой

        # Увеличиваем счетчик при создании каждой новой категории
        Category.category_count += 1

    def add_product(self, product: Product):
        """Метод для добавления товара в категорию."""
        self.products.append(product)
