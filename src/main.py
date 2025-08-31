import json
from abc import ABC, abstractmethod


class InfoMixin:
    """Миксин, который выводит информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        print(f"Создан объект {self.__class__.__name__} с параметрами {args} {kwargs}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Product(InfoMixin, BaseProduct):
    """Класс продукта."""
    all_products = []

    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        Product.all_products.append(self)
        self.__price = price

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return (f"Product('{self.name}', '{self.description}', "
                f"{self.__price}, {self.quantity})")

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Складывать можно только объекты одного класса")
        return (self.__price * self.quantity) + (other.__price * other.quantity)


    @classmethod
    def new_product(cls, product_data, products_list=None):
        """Создает новый продукт на основе данных из словаря."""
        name = product_data.get('name', 'Неизвестный товар')
        description = product_data.get('description', '')
        price = product_data.get('price', 0.0)
        quantity = product_data.get('quantity', 0)

        # Используем переданный список или общий список
        # всех продуктов
        search_list = products_list if (
                products_list is not None) else cls.all_products

        # Проверка на дубликаты
        for existing_product in search_list:
            if existing_product.name == name:
                # Объединяем количество
                existing_product.quantity += quantity
                # Выбираем максимальную цену
                if price > existing_product.__price:
                    existing_product.__price = price
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

        # Проверка на
        # понижение цены
        if new_price < self.__price:
            confirmation = input("Вы уверены, "
                                 "что хотите понизить цену? (y/n): ")
            if confirmation.lower() != 'y':
                print("Отмена изменения цены.")
                return

        self.__price = new_price


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(self, name, description, price, quantity,
                 efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(self, name, description, price, quantity,
                 country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
        """Строковое представление категории с общим количеством товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор для продуктов категории."""
        return CategoryIterator(self.__products)

    def add_product(self, product):
        """Добавляет продукт в
         категорию только если это Product или его наследник."""
        if isinstance(product, Product) and issubclass(type(product), Product):
            self._Category__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять "
                            "только объекты класса Product или его наследников")

    @property
    def products(self):
        """Геттер для списка продуктов в виде строк."""
        if not self.__products:
            return ""
        return "\n".join([str(product) for product in self.__products])

    def get_total_quantity(self):
        """Возвращает общее количество товаров в категории."""
        return sum(product.quantity for product in self.__products)


class CategoryIterator:
    """Класс-итератор для перебора товаров в категории."""

    def __init__(self, products):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration


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
        # Используем get с значениями
        # по умолчанию для обработки отсутствующих ключей
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

    # Демонстрация строкового представления продуктов
    print("Строковое представление продуктов:")
    print(str(product1))
    print(str(product2))
    print(str(product3))
    print()

    # Создание категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    # Демонстрация строкового представления категории
    print("Строковое представление категории:")
    print(str(category1))
    print()

    # Демонстрация свойства products
    print("Список продуктов в категории:")
    print(category1.products)
    print()

    # Демонстрация сложения продуктов
    print("Сложение продуктов:")
    print(f"product1 + product2 = {product1 + product2}")
    print(f"product1 + product3 = {product1 + product3}")
    print(f"product2 + product3 = {product2 + product3}")
    print()

    # Демонстрация итерации по категории
    print("Итерация по категории:")
    for product in category1:
        print(f"  - {product}")
    print()

    # Проверка атрибутов класса
    print("Статистика:")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")


if __name__ == "__main__":
    main()
