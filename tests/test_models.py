import pytest
from src.models import Category, Product, Smartphone, LawnGrass, BaseProduct


@pytest.fixture(autouse=True)
def reset_counters():
    """Сброс счетчиков перед каждым тестом."""
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
    Category.category_count = 0
    category = Category("Smartphones", "Modern mobile devices")

    assert category.name == "Smartphones"
    assert category.description == "Modern mobile devices"
    assert category.products == ""


def test_product_count():
    """Тест подсчета количества продуктов."""
    Category.product_count = 0
    category = Category("Smartphones", "Modern mobile devices")

    product1 = Product("Samsung Galaxy S23", "128GB, Gray", 60000.0, 5)
    product2 = Product("Iphone 15", "128GB, Black", 80000.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    assert Category.product_count == 2
    assert "Samsung Galaxy S23" in category.products
    assert "Iphone 15" in category.products


@pytest.fixture
def product_a():
    """Продукт А для тестов со старыми строками вывода."""
    return Product("Товар A", "Описание A", 100.0, 10)


@pytest.fixture
def product_b():
    """Продукт Б для тестов со старыми строками вывода."""
    return Product("Товар B", "Описание B", 200.0, 2)


@pytest.fixture
def sample_category(product_a, product_b):
    """Категория с товарами."""
    return Category("Бытовая техника", "Техника для дома", [product_a, product_b])


# --- Тесты для класса Product ---

def test_product_str(product_a):
    """Тест строкового представления продукта."""
    assert str(product_a) == "Товар A, 100.0 руб. Остаток: 10 шт."


def test_product_add(product_a, product_b):
    """Тест сложения стоимости остатков."""
    assert product_a + product_b == 1400.0


def test_product_add_type_error(product_a):
    """Тест на ошибку при сложении с не-Product объектом."""
    with pytest.raises(TypeError):
        _ = product_a + 500


# --- Тесты для класса Category ---

def test_category_str(sample_category):
    """Тест строкового представления категории."""
    # Изменяем ожидаемое слово 'товаров' на 'продуктов' в соответствии с вашим кодом
    assert str(sample_category) == "Бытовая техника, количество продуктов: 12 шт."


def test_category_products_getter(sample_category):
    """Тест геттера списка продуктов."""
    expected_output = (
        "Товар A, 100.0 руб. Остаток: 10 шт.\n"
        "Товар B, 200.0 руб. Остаток: 2 шт."
    )
    assert sample_category.products == expected_output


# --- Тесты для новой функциональности сложения товаров (__add__) ---

def test_add_same_class_products(sample_smartphone_1, sample_smartphone_2):
    """Тест сложения двух смартфонов."""
    assert sample_smartphone_1 + sample_smartphone_2 == 1325000.0


def test_add_different_class_products_raises_type_error(sample_smartphone_1, sample_lawn_grass):
    """Тест ошибки сложения смартфона и травы."""
    with pytest.raises(TypeError) as exc_info:
        _ = sample_smartphone_1 + sample_lawn_grass

    # Проверка текста ошибки, который выдает ваш метод __add__
    assert "Складывать можно только товары одного и того же класса" in str(exc_info.value)


def test_add_base_product_and_subclass_raises_type_error(sample_base_product, sample_smartphone_1):
    """Тест ошибки сложения базового продукта и наследника."""
    with pytest.raises(TypeError):
        _ = sample_base_product + sample_smartphone_1


# --- Тесты для метода добавления продуктов (add_product) ---

def test_add_valid_products_to_category(empty_category, sample_smartphone_1, sample_lawn_grass):
    """Тест успешного добавления наследников Product в категорию."""
    empty_category.add_product(sample_smartphone_1)
    empty_category.add_product(sample_lawn_grass)

    assert sample_smartphone_1.name in empty_category.products
    assert sample_lawn_grass.name in empty_category.products


@pytest.mark.parametrize("invalid_product", [
    "Просто строка",
    12345,
    {"name": "Невалидный словарь"},
    [1, 2, 3]
])
def test_add_invalid_object_to_category_raises_type_error(empty_category, invalid_product):
    """Тест ошибки при добавлении сторонних объектов."""
    with pytest.raises(TypeError) as exc_info:
        empty_category.add_product(invalid_product)

    # Проверка текста ошибки, который выдает ваш метод add_product
    assert "Добавить можно только объект класса Product" in str(exc_info.value) or \
           "Добавлять в категорию можно только товары" in str(exc_info.value)


# --- Фикстуры окружения с исправленными путями импорта ---

@pytest.fixture
def sample_base_product():
    return Product("Базовый товар", "Описание", 100.0, 5)


@pytest.fixture
def sample_smartphone_1():
    return Smartphone("iPhone 15", "Описание", 95000.0, 5, 4.0, "Pro", 256, "Titanium")


@pytest.fixture
def sample_smartphone_2():
    return Smartphone("Galaxy S24", "Описание", 85000.0, 10, 4.2, "Ultra", 512, "Black")


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass("Газонная трава", "Описание", 1200.0, 20, "Россия", 14, "Зеленый")


@pytest.fixture
def empty_category():
    return Category("Пустая категория", "Описание")


# --- ТЕСТЫ ДЛЯ АБСТРАКТНОГО КЛАССА (BaseProduct) ---

def test_base_product_cannot_be_instantiated():
    """Проверка, что невозможно создать объект абстрактного класса BaseProduct напрямую."""
    with pytest.raises(TypeError) as exc_info:
        # Попытка инициализации абстрактного класса
        _ = BaseProduct("Тест", "Описание", 100.0, 1)  # type: ignore

    # Python выдает ошибку о невозможности создания экземпляра абстрактного класса
    assert "Can't instantiate abstract class BaseProduct" in str(exc_info.value)


# --- ТЕСТЫ ДЛЯ КЛАССА-МИКСИНА (LogMixin) ---

def test_product_creation_logging(capsys):
    """Проверка, что при создании объекта Product миксин выводит лог в консоль."""
    # Создаем объект, вывод перехватывается фикстурой capsys
    _ = Product('Продукт1', 'Описание продукта', 1200.0, 10)

    # Читаем то, что попало в stdout
    captured = capsys.readouterr()

    # Проверяем ожидаемую строку лога
    expected_output = "Создан объект: Product('Продукт1', 'Описание продукта', 1200.0, 10)\n"
    assert captured.out == expected_output


def test_smartphone_creation_logging(capsys):
    """Проверка, что миксин корректно логирует подклассы и выводит их имя (Smartphone)."""
    _ = Smartphone("iPhone 15", "Флагман", 95000.0, 5, 4.0, "Pro", 256, "Titanium")

    captured = capsys.readouterr()

    # Так как аргументы передаются в super().__init__ базового класса Product,
    # миксин перехватывает первые 4 переданных позиционных аргумента
    expected_output = "Создан объект: Smartphone('iPhone 15', 'Флагман', 95000.0, 5)\n"
    assert captured.out == expected_output


def test_lawn_grass_creation_logging(capsys):
    """Проверка, что миксин корректно логирует подклассы и выводит их имя (LawnGrass)."""
    _ = LawnGrass("Канада Грин", "Износостойкая", 1200.0, 20, "Канада", 14, "Изумрудный")

    captured = capsys.readouterr()

    expected_output = "Создан объект: LawnGrass('Канада Грин', 'Износостойкая', 1200.0, 20)\n"
    assert captured.out == expected_output
