import pytest
from src.models import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Product.product_count = 0


def test_product_initialization():
    """Тест корректности инициализации объекта Product."""
    product = Product("Смартфон", "Флагманский телефон", 75000.0, 10)

    assert product.name == "Смартфон"
    assert product.description == "Флагманский телефон"
    assert product.price == 75000.0
    assert product.quantity == 10


def test_category_initialization():
    """Тест корректности инициализации объекта Category."""
    category = Category("Электроника", "Гаджеты и аксессуары")

    assert category.name == "Электроника"
    assert category.description == "Гаджеты и аксессуары"
    assert category.products == []


def test_category_count():
    """Тест подсчета количества созданных категорий."""
    assert Category.category_count == 0

    cat1 = Category("Электроника", "Гаджеты")
    assert Category.category_count == 1

    cat2 = Category("Книги", "Художественная литература")
    assert Category.category_count == 2


def test_product_count():
    """Тест подсчета количества созданных уникальных продуктов."""
    assert Product.product_count == 0

    prod1 = Product("Смартфон", "Телефон", 75000.0, 10)
    assert Product.product_count == 1

    prod2 = Product("Чехол", "Аксессуар", 1200.0, 50)
    assert Product.product_count == 2
