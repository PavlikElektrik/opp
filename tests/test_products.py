import pytest
from src.main import Product, Category, ZeroQuantityError


def test_product_creation_with_zero_quantity():
    """Тест создания товара с нулевым количеством."""
    with pytest.raises(ZeroQuantityError):
        Product("Test Product", "Description", 100.0, 0)


def test_middle_price_with_products():
    """Тест расчета средней цены в категории с товарами."""
    product1 = Product("Product1", "Desc1", 100.0, 5)
    product2 = Product("Product2", "Desc2", 200.0, 3)
    category = Category("Test Category", "Description", [product1, product2])

    assert category.middle_price() == 150.0


def test_middle_price_empty_category():
    """Тест расчета средней цены в пустой категории."""
    category = Category("Empty Category", "Description", [])

    assert category.middle_price() == 0


def test_add_product_with_zero_quantity():
    """Тест добавления товара с нулевым количеством в категорию."""
    product = Product("Test Product", "Description", 100.0, 1)
    product.quantity = 0  # Изменяем количество на 0 после создания
    category = Category("Test Category", "Description")

    # Не должно вызывать исключение, но должно выводить сообщение об ошибке
    category.add_product(product)
    assert len(category.products) == 0
