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
    """Тест первоначальной инициализации объекта класса Category."""
    # Сбрасываем счетчик перед тестом, если это необходимо
    Category.category_count = 0

    category = Category("Smartphones", "Modern mobile devices")

    assert category.name == "Smartphones"
    assert category.description == "Modern mobile devices"
    # Исправлено: геттер возвращает пустую строку, а не пустой список
    assert category.products == ""


def test_product_count():
    """Тест подсчета количества продуктов."""
    # Сбрасываем счетчик перед тестом, чтобы прошлые тесты не влияли на результат
    Category.product_count = 0

    category = Category("Smartphones", "Modern mobile devices")

    product1 = Product("Samsung Galaxy S23", "128GB, Gray", 60000.0, 5)
    product2 = Product("Iphone 15", "128GB, Black", 80000.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Исправлено: проверяем количество через счетчик класса,
    # так как len(category.products) считает символы в строке
    assert Category.product_count == 2

    # Дополнительно проверяем, что продукты отображаются в строке корректно
    assert "Samsung Galaxy S23" in category.products
    assert "Iphone 15" in category.products

@pytest.fixture
def product_a():
    """Фикстура для товара A."""
    return Product("Товар A", "Описание A", 100.0, 10)


@pytest.fixture
def product_b():
    """Фикстура для товара B."""
    return Product("Товар B", "Описание B", 200.0, 2)


@pytest.fixture
def sample_category(product_a, product_b):
    """Фикстура для категории с двумя товарами."""
    return Category("Электроника", "Гаджеты и девайсы", [product_a, product_b])


# --- Тесты для класса Product ---

def test_product_str(product_a):
    """Тест строкового отображения продукта."""
    assert str(product_a) == "Товар A, 100.0 руб. Остаток: 10 шт."


def test_product_add(product_a, product_b):
    """Тест сложения двух продуктов (полная стоимость на складе)."""
    # 100 * 10 + 200 * 2 = 1000 + 400 = 1400
    assert product_a + product_b == 1400.0


def test_product_add_type_error(product_a):
    """Тест, что сложение товара с объектом другого типа вызывает ошибку."""
    with pytest.raises(TypeError):
        _ = product_a + 500  # Попытка сложить товар с числом


# --- Тесты для класса Category ---

def test_category_str(sample_category):
    """Тест строкового отображения категории (подсчет общего количества штук)."""
    # 10 шт товара A + 2 шт товара B = 12 шт
    assert str(sample_category) == "Электроника, количество продуктов: 12 шт."


def test_category_products_getter(sample_category):
    """Тест работы геттера продуктов через str()."""
    expected_output = (
        "Товар A, 100.0 руб. Остаток: 10 шт.\n"
        "Товар B, 200.0 руб. Остаток: 2 шт."
    )
    assert sample_category.products == expected_output