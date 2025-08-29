import json
import os


class Product:
    """Класс для представления товара."""
    all_products = []

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.all_products.append(self)

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return (f"Product('{self.name}', '{self.description}', "
                f"{self.__price}, {self.quantity})")

    @classmethod
    def new_product(cls, product_data, products_list=None):
        """Создает новый продукт на основе данных из словаря."""
        name = product_data.get('name', 'Неизвестный товар')
        description = product_data.get('description', '')
        price = product_data.get('price', 0.0)
        quantity = product_data.get('quantity', 0)

        # Используем переданный список или общий список всех продуктов
        search_list = products_list if products_list is not None else cls.all_products

        # Проверка на дубликаты
        for existing_product in search_list:
            if existing_product.name == name:
                # Объединяем количество
                existing_product.quantity += quantity
                # Выбираем максимальную цену
                if price > existing_product.price:
                    existing_product.price = price
                return existing_product

        return cls(name, description, price, quantity)

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой валидности."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Проверка на понижение цены
        if new_price < self.__price:
            confirmation = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if confirmation.lower() != 'y':
                print("Отмена изменения цены.")
                return

        self.__price = new_price


class Category:
    """Класс для представления категории товаров."""
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)}"

    def add_product(self, product):
        """Добавляет продукт в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        """Геттер для списка продуктов в виде строк."""
        if not self.__products:
            return ""
        return "\n".join([str(product) for product in self.__products])


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
        # Используем get с значениями по умолчанию для обработки отсутствующих ключей
        products = []
        for product_data in category_data.get('products', []):
            product = Product(
                product_data.get('name', 'Неизвестный товар'),
                product_data.get('description', ''),
                product_data.get('price', 0.0),
                product_data.get('quantity', 0)
            )
            products.append(product)

        category = Category(
            category_data.get('name', 'Неизвестная категория'),
            category_data.get('description', ''),
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
    print(len(category1._Category__products))
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
    print(len(category2._Category__products))
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
            print(f"Категория: {category.name}, продуктов: {len(category._Category__products)}")

    # Демонстрация новой функциональности
    print("\n--- Демонстрация новой функциональности ---")

    # Добавление продукта в категорию
    new_product = Product("Test Product", "Test Description", 1000.0, 10)
    category1.add_product(new_product)
    print(f"\nПосле добавления продукта: {len(category1._Category__products)} товаров в категории")

    # Создание продукта через класс-метод
    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 500.0,
        "quantity": 3
    }
    new_product_2 = Product.new_product(product_data)
    print(f"\nСозданный продукт: {new_product_2.name}, {new_product_2.price} руб.")

    # Проверка работы с ценой
    print(f"\nТекущая цена: {new_product_2.price}")
    new_product_2.price = 600.0  # Увеличение цены
    print(f"Новая цена после увеличения: {new_product_2.price}")

    # Попытка установить невалидную цену
    new_product_2.price = -100.0
    print(f"Цена после попытки установить отрицательное значение: {new_product_2.price}")

    # Попытка установить нулевую цену
    new_product_2.price = 0
    print(f"Цена после попытки установить нулевое значение: {new_product_2.price}")


if __name__ == "__main__":
    main()

