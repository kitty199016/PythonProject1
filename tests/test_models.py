import pytest
from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    """Фикстура для сброса счетчиков перед каждым тестом.

    Это необходимо, так как атрибуты класса сохраняют состояния между тестами.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест корректности инициализации объекта класса Product."""
    product = Product("Samsung Galaxy S23", "128GB, Gray", 60000.0, 5)

    assert product.name == "Samsung Galaxy S23"
    assert product.description == "128GB, Gray"
    assert product.price == 60000.0
    assert product.quantity == 5


def test_category_initialization():
    """Тест корректности инициализации объекта класса Category."""
    category = Category("Smartphones", "Modern mobile devices")

    assert category.name == "Smartphones"
    assert category.description == "Modern mobile devices"
    assert category.products == []


def test_product_count():
    """Тест подсчета количества продуктов."""
    category = Category("Smartphones", "Modern mobile devices")

    product1 = Product("Samsung Galaxy S23", "128GB, Gray", 60000.0, 5)
    product2 = Product("Iphone 15", "128GB, Black", 80000.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Проверяем, что в списке категории 2 товара
    assert len(category.products) == 2
    # Проверяем счетчик класса Category
    assert Category.product_count == 2


def test_category_count():
    """Тест подсчета количества категорий."""
    category1 = Category("Smartphones", "Modern mobile devices")
    category2 = Category("TVs", "Modern smart TVs")

    # Проверяем счетчик класса Category
    assert Category.category_count == 2
