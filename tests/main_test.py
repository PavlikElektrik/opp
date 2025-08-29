import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch
from src.main import Product, Category, load_data_from_json, main

# Добавляем путь к исходному коду для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(autouse=True)
def reset_category_count():
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


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
    assert len(category.products) == 1
    assert category.products[0].name == "Test Product"


def test_category_string_representation():
    """Тест строкового представления категории."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    category = Category("Test Category", "Test Description", [product])
    expected_string = "Test Category, количество продуктов: 1"

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
    assert len(category.products) == 0
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
    assert isinstance(category.products, list)


def test_category_with_multiple_products():
    """Тест категории с несколькими продуктами."""
    products = [
        Product("Product1", "Desc1", 100.0, 1),
        Product("Product2", "Desc2", 200.0, 2),
        Product("Product3", "Desc3", 300.0, 3)
    ]

    category = Category("Test Category", "Test Description", products)

    assert len(category.products) == 3
    assert category.products[0].name == "Product1"
    assert category.products[1].name == "Product2"
    assert category.products[2].name == "Product3"


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
        assert len(categories[0].products) == 2
        assert categories[0].products[0].name == "Test Product 1"
        assert categories[0].products[1].name == "Test Product 2"
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
        assert len(categories[0].products) == 1
        assert categories[0].products[0].name == "Test Product 1"
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
    assert "Телевизоры" in captured.out


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
