import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch
from src.main import (Product, Category,
                      load_data_from_json, main,
                      CategoryIterator, Smartphone,
                      LawnGrass, ZeroQuantityError)

# Добавляем путь к исходному коду для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(autouse=True)
def reset_class_variables():
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    Product.all_products = []
    yield
    Category.category_count = 0
    Category.product_count = 0
    Product.all_products = []


def test_product_initialization():
    """Тест инициализации продукта."""
    product = Product("Test Product", "Test Description", 100.0, 10)

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_product_string_representation():
    """Тест строкового представления продукта."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    expected_string = "Test Product, 100.0 руб. Остаток: 10 шт."

    assert str(product) == expected_string


def test_product_repr_representation():
    """Тест представления продукта для отладки."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    expected_repr = ("Product('Test Product', 'Test Description', "
                     "100.0, 10)")

    assert repr(product) == expected_repr


def test_category_initialization():
    """Тест инициализации категории."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    category = Category("Test Category", "Test Description", [product])

    assert category.name == "Test Category"
    assert category.description == "Test Description"
    assert len(category._Category__products) == 1
    assert "Test Product" in category.products


def test_category_string_representation():
    """Тест строкового представления категории."""
    product1 = Product("Product1",
                       "Desc1",
                       100.0,
                       5)
    product2 = Product("Product2",
                       "Desc2",
                       200.0,
                       3)
    category = Category("Test Category",
                        "Test Description",
                        [product1, product2])

    # Ожидаем общее количество товаров (5 + 3 = 8)
    expected_string = "Test Category, количество продуктов: 8 шт."

    assert str(category) == expected_string


def test_category_count_single_category():
    """Тест подсчета категорий и продуктов для одной категории."""
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)

    Category("Test Category", "Test Description",
             [product1, product2])

    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_count_multiple_categories():
    """Тест подсчета категорий и продуктов для нескольких категорий."""
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)
    product3 = Product("Product3", "Desc3", 300.0, 3)

    Category("Category1", "Description1", [product1, product2])
    Category("Category2", "Description2", [product3])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_empty_category():
    """Тест создания категории без продуктов."""
    category = Category("Empty Category", "Empty Description", [])

    assert category.name == "Empty Category"
    assert len(category._Category__products) == 0
    assert category.products == ""
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_attributes_types():
    """Тест типов данных атрибутов продукта."""
    product = Product("Test", "Test", 100.0, 10)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_category_attributes_types():
    """Тест типов данных атрибутов категории."""
    product = Product("Test", "Test", 100.0, 10)
    category = Category("Test", "Test", [product])

    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, str)


def test_category_with_multiple_products():
    """Тест категории с несколькими продуктами."""
    products = [
        Product("Product1", "Desc1", 100.0, 1),
        Product("Product2", "Desc2", 200.0, 2),
        Product("Product3", "Desc3", 300.0, 3)
    ]

    category = Category("Test Category", "Test Description", products)

    assert len(category._Category__products) == 3
    assert "Product1" in category.products
    assert "Product2" in category.products
    assert "Product3" in category.products


def test_load_data_from_json():
    """Тест загрузки данных из JSON файла."""
    # Создаем временный файл с тестовыми данными
    test_data = [
        {
            "name": "Test Category",
            "description": "Test Description",
            "products": [
                {
                    "name": "Test Product 1",
                    "description": "Test Description 1",
                    "price": 100.0,
                    "quantity": 5
                },
                {
                    "name": "Test Product 2",
                    "description": "Test Description 2",
                    "price": 200.0,
                    "quantity": 10
                }
            ]
        }
    ]

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                     delete=False) as f:
        json.dump(test_data, f)
        temp_file_path = f.name

    try:
        # Загружаем данные из временного файла
        categories = load_data_from_json(temp_file_path)

        # Проверяем результаты
        assert len(categories) == 1
        assert categories[0].name == "Test Category"
        assert categories[0].description == "Test Description"
        assert len(categories[0]._Category__products) == 2
        assert "Test Product 1" in categories[0].products
        assert "Test Product 2" in categories[0].products
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_data_from_json_file_not_found():
    """Тест загрузки данных из несуществующего JSON файла."""
    with patch('builtins.print') as mock_print:
        categories = load_data_from_json("non_existent_file.json")

        # Проверяем, что возвращается пустой список
        assert categories == []

        # Проверяем, что было выведено сообщение об ошибке
        expected_call = ("Файл non_existent_file.json не найден, "
                         "пропускаем загрузку из JSON")
        mock_print.assert_called_with(expected_call)


def test_load_data_from_json_invalid_json():
    """Тест загрузки данных из невалидного JSON файла."""
    # Создаем временный файл с невалидными данными
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                     delete=False) as f:
        f.write('{"invalid": json}')
        temp_file_path = f.name

    try:
        with patch('builtins.print') as mock_print:
            categories = load_data_from_json(temp_file_path)

            # Проверяем, что возвращается пустой список
            assert categories == []

            # Проверяем, что было выведено сообщение об ошибке
            expected_call = (f"Ошибка декодирования JSON в файле "
                             f"{temp_file_path}")
            mock_print.assert_called_with(expected_call)
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_data_from_json_missing_keys():
    """Тест загрузки данных из JSON файла с отсутствующими ключами."""
    # Создаем временный файл с неполными данными
    test_data = [
        {
            "name": "Test Category",
            "description": "Test Description",
            "products": [
                {
                    "name": "Test Product 1",
                    "description": "Test Description 1",
                    "price": 100.0,
                    "quantity": 5
                }
            ]
        }
    ]

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                     delete=False) as f:
        json.dump(test_data, f)
        temp_file_path = f.name

    try:
        categories = load_data_from_json(temp_file_path)

        # Проверяем, что категория создалась
        assert len(categories) == 1
        assert categories[0].name == "Test Category"
        assert categories[0].description == "Test Description"
        assert len(categories[0]._Category__products) == 1
        assert "Test Product 1" in categories[0].products
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_main_execution(capsys):
    """Тест выполнения основного блока кода."""
    # Вызываем основную функцию
    main()

    # Перехватываем вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемые данные
    assert "Samsung Galaxy S23 Ultra" in captured.out
    assert "Iphone 15" in captured.out
    assert "Xiaomi Redmi Note 11" in captured.out
    assert "Смартфоны" in captured.out


def test_class_variables_independence():
    """Тест независимости переменных класса между экземплярами."""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Создаем первую категорию
    product1 = Product("Product1", "Desc1", 100.0, 1)
    category1 = Category("Category1", "Desc1", [product1])

    assert Category.category_count == 1
    assert Category.product_count == 1

    # Создаем вторую категорию
    product2 = Product("Product2", "Desc2", 200.0, 2)
    product3 = Product("Product3", "Desc3", 300.0, 3)
    category2 = Category("Category2", "Desc2", [product2, product3])

    assert Category.category_count == 2
    assert Category.product_count == 3

    # Проверяем, что переменные класса доступны через экземпляры
    assert category1.category_count == 2
    assert category1.product_count == 3
    assert category2.category_count == 2
    assert category2.product_count == 3


def test_private_products_attribute():
    """Тест приватного атрибута продуктов в категории."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    category = Category("Test Category", "Test Description", [product])

    # Проверяем, что доступ к приватному атрибуту невозможен напрямую
    with pytest.raises(AttributeError):
        _ = category.__products


def test_add_product_method():
    """Тест метода add_product."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    category = Category("Test Category", "Test Description", [])

    # Добавляем продукт
    category.add_product(product)

    # Проверяем, что продукт добавлен
    assert len(category._Category__products) == 1
    assert "Test Product" in category.products
    assert Category.product_count == 1


def test_add_product_invalid_type():
    """Тест добавления невалидного типа в категорию."""
    category = Category("Test Category", "Test Description", [])

    # Пытаемся добавить не продукт
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_products_property():
    """Тест свойства products."""
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)

    category = Category("Test Category", "Test Description",
                        [product1, product2])

    # Проверяем, что свойство возвращает строку
    assert isinstance(category.products, str)

    # Проверяем формат вывода
    assert "Product1, 100.0 руб. Остаток: 1 шт." in category.products
    assert "Product2, 200.0 руб. Остаток: 2 шт." in category.products


def test_new_product_class_method():
    """Тест класс-метода new_product."""
    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 100.0,
        "quantity": 5
    }

    # Создаем продукт через класс-метод
    product = Product.new_product(product_data)

    # Проверяем, что продукт создан правильно
    assert product.name == "New Product"
    assert product.description == "New Description"
    assert product.price == 100.0
    assert product.quantity == 5


def test_new_product_duplicate():
    """Тест класс-метода new_product с дубликатом."""
    # Создаем первый продукт
    product1 = Product("Duplicate Product", "Description", 100.0, 5)

    # Создаем второй продукт с тем же именем через класс-метод
    product_data = {
        "name": "Duplicate Product",
        "description": "New Description",
        "price": 150.0,
        "quantity": 3
    }

    product2 = Product.new_product(product_data)

    # Проверяем, что вернулся первый продукт с обновленными значениями
    assert product2 is product1
    assert product2.quantity == 8  # 5 + 3
    assert product2.price == 150.0  # Выбрана максимальная цена


def test_price_getter_setter():
    """Тест геттера и сеттера для цены."""
    product = Product("Test Product", "Test Description", 100.0, 10)

    # Проверяем геттер
    assert product.price == 100.0

    # Устанавливаем новую цену через сеттер
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_invalid():
    """Тест сеттера для невалидной цены."""
    product = Product("Test Product", "Test Description", 100.0, 10)

    # Пытаемся установить отрицательную цену
    with patch('builtins.print') as mock_print:
        product.price = -50.0
        assert product.price == 100.0  # Цена не изменилась
        mock_print.assert_called_with("Цена не должна "
                                      "быть нулевая или отрицательная")

    # Пытаемся установить нулевую цену
    with patch('builtins.print') as mock_print:
        product.price = 0
        assert product.price == 100.0  # Цена не изменилась
        mock_print.assert_called_with("Цена не должна"
                                      " быть нулевая или отрицательная")


def test_price_setter_decrease_with_confirmation():
    """Тест сеттера для понижения цены с подтверждением."""
    product = Product("Test Product", "Test Description", 100.0, 10)

    # Мокаем input для подтверждения
    with patch('builtins.input', return_value='y'):
        product.price = 80.0
        assert product.price == 80.0  # Цена изменилась

    # Мокаем input для отмены
    with patch('builtins.input', return_value='n'):
        product.price = 70.0
        assert product.price == 80.0  # Цена не изменилась


def test_all_products_class_variable():
    """Тест атрибута класса all_products."""
    # Очищаем список перед тестом
    Product.all_products = []

    # Создаем продукты
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)

    # Проверяем, что продукты добавлены в all_products
    assert len(Product.all_products) == 2
    assert product1 in Product.all_products
    assert product2 in Product.all_products


def test_products_property_empty_category():
    """Тест свойства products для пустой категории."""
    category = Category("Test Category", "Test Description", [])
    assert category.products == ""


def test_product_addition():
    """Тест сложения продуктов."""
    product1 = Product("Product1", "Desc1", 100.0, 2)
    product2 = Product("Product2", "Desc2", 200.0, 3)

    # Проверяем сложение продуктов
    result = product1 + product2
    expected = (100.0 * 2) + (200.0 * 3)  # 200 + 600 = 800
    assert result == expected


def test_product_addition_invalid_type():
    """Тест сложения продукта с неверным типом."""
    product = Product("Product", "Desc", 100.0, 2)

    # Пытаемся сложить продукт с не продуктом
    with pytest.raises(TypeError):
        _ = product + "not a product"


def test_category_iterator():
    """Тест итератора категории."""
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)
    product3 = Product("Product3", "Desc3", 300.0, 3)

    category = Category("Test Category", "Test Description",
                        [product1, product2, product3])

    # Проверяем итерацию по категории
    products_from_iteration = []
    for product in category:
        products_from_iteration.append(product)

    assert len(products_from_iteration) == 3
    assert products_from_iteration[0] == product1
    assert products_from_iteration[1] == product2
    assert products_from_iteration[2] == product3


def test_category_iterator_empty():
    """Тест итератора для пустой категории."""
    category = Category("Test Category", "Test Description", [])

    # Проверяем итерацию по пустой категории
    products_from_iteration = []
    for product in category:
        products_from_iteration.append(product)

    assert len(products_from_iteration) == 0


def test_category_iterator_class():
    """Тест класса-итератора категории."""
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)

    iterator = CategoryIterator([product1, product2])

    # Проверяем итерацию
    products_from_iteration = []
    for product in iterator:
        products_from_iteration.append(product)

    assert len(products_from_iteration) == 2
    assert products_from_iteration[0] == product1
    assert products_from_iteration[1] == product2


def test_category_total_quantity():
    """Тест метода get_total_quantity."""
    product1 = Product("Product1", "Desc1", 100.0, 5)
    product2 = Product("Product2", "Desc2", 200.0, 3)

    category = Category("Test Category",
                        "Test Description",
                        [product1, product2])

    # Проверяем общее количество товаров
    total_quantity = category.get_total_quantity()
    assert total_quantity == 8  # 5 + 3


def test_product_addition_multiple():
    """Тест сложения нескольких продуктов."""
    product1 = Product("Product1", "Desc1", 100.0, 2)
    product2 = Product("Product2", "Desc2", 200.0, 3)
    product3 = Product("Product3", "Desc3", 300.0, 4)

    # Правильное сложение нескольких продуктов - попарно
    result = (product1 + product2) + (product3.price * product3.quantity)
    expected = (100.0 * 2) + (200.0 * 3) + (300.0 * 4)
    # 200 + 600 + 1200 = 2000
    assert result == expected


def test_product_addition_with_price_change():
    """Тест сложения продуктов после изменения цены."""
    product1 = Product("Product1", "Desc1", 100.0, 2)
    product2 = Product("Product2", "Desc2", 200.0, 3)

    # Запоминаем первоначальную сумму
    initial_sum = product1 + product2

    # Меняем цену первого продукта
    product1.price = 150.0

    # Проверяем, что сумма изменилась корректно
    new_sum = product1 + product2
    expected = (150.0 * 2) + (200.0 * 3)  # 300 + 600 = 900
    assert new_sum == expected
    assert new_sum != initial_sum


def test_smartphone_initialization():
    smartphone = Smartphone("Test Phone",
                            "Desc",
                            1000.0,
                            3,
                            95.5,
                            "ModelX",
                            128,
                            "Black")
    assert smartphone.name == "Test Phone"
    assert smartphone.model == "ModelX"
    assert smartphone.memory == 128
    assert smartphone.color == "Black"


def test_lawngrass_initialization():
    grass = LawnGrass("Grass",
                      "Desc",
                      500.0,
                      10,
                      "Россия",
                      "7 дней",
                      "Зеленый")
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_addition_same_class():
    s1 = Smartphone("Phone1", "Desc", 100.0, 2, 90.0, "M1", 64, "Gray")
    s2 = Smartphone("Phone2", "Desc", 200.0, 3, 95.0, "M2", 128, "Black")
    assert s1 + s2 == (100.0 * 2) + (200.0 * 3)


def test_addition_different_class_raises():
    s1 = Smartphone("Phone1", "Desc", 100.0, 2, 90.0, "M1", 64, "Gray")
    g1 = LawnGrass("Grass", "Desc", 500.0, 1, "Россия", "7 дней", "Green")
    with pytest.raises(TypeError):
        _ = s1 + g1


def test_add_invalid_type_to_category():
    c = Category("Test", "Desc", [])
    with pytest.raises(TypeError):
        c.add_product("not a product")


@pytest.fixture
def sample_product():
    return Product("Samsung Galaxy S23 Ultra",
                   "256GB, Серый цвет,"
                   " 200MP камера",
                   180000.0,
                   5)


@pytest.fixture
def smartphone():
    return Smartphone(
        "Iphone 15",
        "512GB,"
        " Gray space",
        210000.0,
        8,
        efficiency=90,
        model="Pro",
        memory=256,
        color="Gray"
    )


@pytest.fixture
def lawn_grass():
    # Это какой-то другой класс, не Product
    return "not a product"  # Пример объекта, который не является Product


def test_lawn_grass_creation(lawn_grass):
    lawn_grass = LawnGrass("Трава газонная",
                           "Описание",
                           100, 50,
                           "Russia",
                           7,
                           "Green")
    assert lawn_grass.name == "Трава газонная"
    assert lawn_grass.country == "Russia"
    assert lawn_grass.germination_period == 7
    assert lawn_grass.color == "Green"


# Тестируем создание объектов
def test_product_creation(sample_product):
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.price == 180000.0
    assert sample_product.quantity == 5
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"


def test_smartphone_creation(smartphone):
    assert smartphone.name == "Iphone 15"
    assert smartphone.efficiency == 90
    assert smartphone.memory == 256
    assert smartphone.color == "Gray"


# Тестируем работу миксина (информация при создании объекта)
def test_info_mixin(capsys):
    Product("Test Product", "Test Description", 1000.0, 10)
    captured = capsys.readouterr()
    assert "Создан объект Product" in captured.out


# Тестируем работу с категориями
def test_add_product_to_category():
    product = Product("Product", "Desc", 100.0, 2)
    category = Category("Category", "Desc", [])

    category.add_product(product)
    assert Category.product_count == 1


def test_add_invalid_product_to_category():
    category = Category("Трава", "Все для сада")
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_category_product_count():
    category = Category("Телевизоры", "Все телевизоры")
    assert Category.product_count == 0  # По умолчанию товаров нет
    category.add_product(Product("Телевизор LG", "4K телевизор", 70000, 2))
    assert Category.product_count == 1


# Добавьте эти тесты в конец вашего тестового файла

def test_product_creation_with_zero_quantity():
    """Тест создания товара с нулевым количеством."""
    with pytest.raises(ZeroQuantityError):
        Product("Test Product", "Description", 100.0, 0)


def test_category_middle_price_with_products():
    """Тест расчета средней цены в категории с товарами."""
    product1 = Product("Product1", "Desc1", 100.0, 5)
    product2 = Product("Product2", "Desc2", 200.0, 3)
    category = Category("Test Category", "Description", [product1, product2])

    assert category.middle_price() == 150.0


def test_category_middle_price_empty_category():
    """Тест расчета средней цены в пустой категории."""
    category = Category("Empty Category", "Description", [])

    assert category.middle_price() == 0


def test_add_product_with_zero_quantity():
    """Тест добавления товара с нулевым количеством в категорию."""
    # Создаем продукт с количеством 1, затем изменяем количество на 0
    product = Product("Test Product", "Description", 100.0, 1)
    product.quantity = 0

    category = Category("Test Category", "Description")

    # Не должно вызывать исключение, но должно выводить сообщение об ошибке
    category.add_product(product)
    assert len(category._Category__products) == 0


def test_zero_quantity_error_message():
    """Тест сообщения об ошибке при создании товара с нулевым количеством."""
    try:
        Product("Test Product", "Description", 100.0, 0)
        assert False, "Должно было быть вызвано исключение ZeroQuantityError"
    except ZeroQuantityError as e:
        assert str(e) == "Товар с нулевым количеством не может быть добавлен"
