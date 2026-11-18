import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker

from marketplace.models import ProductType, Product, Customer, Order, OrderItem


class Command(BaseCommand):
    help = "Генерация тестовых данных"

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        self.stdout.write("Начало генерации данных")

        user = User.objects.filter(is_superuser=True).first() or User.objects.first()

        with transaction.atomic():
            self.stdout.write("Создание типов товаров")
            categories = []
            category_names = [
                "Смартфоны", "Ноутбуки", "Наушники", "Телевизоры", "Планшеты",
                "Фотоаппараты", "Умные часы", "Аксессуары", "Игровые приставки",
                "Мониторы", "Клавиатуры", "Мыши", "Колонки", "Холодильники",
                "Микроволновки", "Пылесосы", "Стиральные машины", "Кофемашины",
                "Чайники", "Утюги"
            ]
            for cat_name in category_names:
                cat, _ = ProductType.objects.get_or_create(name=cat_name)
                categories.append(cat)

            self.stdout.write("Генерация 1000 покупателей")
            customers = []
            for _ in range(1000):
                customer = Customer(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone=fake.phone_number(),
                )
                customers.append(customer)
            Customer.objects.bulk_create(customers)
            saved_customers = list(Customer.objects.all())

            self.stdout.write("Генерация 1000 товаров")
            products = []
            for _ in range(1000):
                product = Product(
                    name=f"{fake.word().capitalize()} {fake.word()}",
                    quantity=random.randint(1, 150),
                    category=random.choice(categories),
                    user=user,
                )
                products.append(product)
            Product.objects.bulk_create(products)
            saved_products = list(Product.objects.all())

            self.stdout.write("Генерация 1000 заказов")
            orders = []
            for _ in range(1000):
                order = Order(
                    customer=random.choice(saved_customers),
                    address=fake.address(),
                )
                orders.append(order)
            Order.objects.bulk_create(orders)
            saved_orders = list(Order.objects.all())

            self.stdout.write("Генерация 1000 позиций заказов")
            order_items = []
            for _ in range(1000):
                item = OrderItem(
                    order=random.choice(saved_orders),
                    product=random.choice(saved_products),
                    count=random.randint(1, 10),
                )
                order_items.append(item)
            OrderItem.objects.bulk_create(order_items)

        self.stdout.write(self.style.SUCCESS("Сгенерировано 1000 записей для всех основных таблиц"))