import json
import os


class Product:
    """Класс для представления товара."""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return (f"Product('{self.name}', '{self.description}', "
                f"{self.price}, {self.quantity})")


class Category:
    """Класс для представления категории товаров."""
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.products)}"


def load_data_from_json(file_path):
    """Загружает данные о категориях и товарах из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден, пропускаем загрузку из JSON")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {file_path}")
        return []

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data['products']:
            product = Product(
                product_data['name'],
                product_data['description'],
                product_data['price'],
                product_data['quantity']
            )
            products.append(product)

        category = Category(
            category_data['name'],
            category_data['description'],
            products
        )
        categories.append(category)

    return categories


def main():
    """Основная функция для демонстрации работы классов."""
    # Создание продуктов
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14
    )

    # Вывод информации о продуктах
    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    # Создание категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    # Проверка категории
    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(Category.category_count)
    print(Category.product_count)

    # Создание второй категории
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, "
        "станет вашим другом и помощником",
        [product4]
    )

    # Проверка второй категории
    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    # Проверка атрибутов класса
    print(Category.category_count)
    print(Category.product_count)

    # Демонстрация работы с JSON
    json_file_path = os.path.join(os.path.dirname(__file__), "products.json")
    categories_from_json = load_data_from_json(json_file_path)

    if categories_from_json:
        print(f"\nЗагружено категорий из JSON: {len(categories_from_json)}")
        for category in categories_from_json:
            print(f"Категория: {category.name}, продуктов: {len(category.products)}")


if __name__ == "__main__":
    main()
