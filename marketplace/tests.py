from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from marketplace.models import ProductType, Product, Customer, Order, OrderItem


class ProductTypesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        item = baker.make(ProductType)
        r = self.client.get('/api/product-types/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['name'] == item.name
        assert data[0]['id'] == item.id

    def test_create_product_type(self):
        r = self.client.post('/api/product-types/', {
            "name": "Электроника"
        })
        new_id = r.json()['id']
        items = ProductType.objects.all()
        assert len(items) == 1
        new_item = ProductType.objects.filter(id=new_id).first()
        assert new_item.name == "Электроника"

    def test_delete_product_type(self):
        items = baker.make(ProductType, 10)
        assert len(ProductType.objects.all()) == 10
        item_id_to_delete = items[3].id

        self.client.delete(f'/api/product-types/{item_id_to_delete}/')

        r = self.client.get('/api/product-types/')
        data = r.json()
        assert len(data) == 9
        assert item_id_to_delete not in [i['id'] for i in data]

    def test_update_product_type(self):
        items = baker.make(ProductType, 10)
        item = items[2]

        self.client.put(f'/api/product-types/{item.id}/', {
            "name": "Новый тип"
        })

        r = self.client.get(f'/api/product-types/{item.id}/')
        data = r.json()
        assert data['name'] == "Новый тип"


class ProductsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        category = baker.make(ProductType)
        product = baker.make(Product, category=category)
        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['name'] == product.name
        assert data[0]['id'] == product.id

    def test_create_product(self):
        category = baker.make(ProductType)
        r = self.client.post('/api/products/', {
            "name": "Клавиатура",
            "quantity": "15",
            "category": category.id
        })
        new_id = r.json()['id']
        products = Product.objects.all()
        assert len(products) == 1
        new_product = Product.objects.filter(id=new_id).first()
        assert new_product.name == "Клавиатура"

    def test_delete_product(self):
        products = baker.make(Product, 10)
        assert len(Product.objects.all()) == 10
        product_id_to_delete = products[3].id

        self.client.delete(f'/api/products/{product_id_to_delete}/')

        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 9
        assert product_id_to_delete not in [i['id'] for i in data]

    def test_update_product(self):
        products = baker.make(Product, 10)
        product = products[2]

        self.client.put(f'/api/products/{product.id}/', {
            "name": "Обновленный товар",
            "quantity": "50"
        })

        r = self.client.get(f'/api/products/{product.id}/')
        data = r.json()
        assert data['name'] == "Обновленный товар"
        assert data['quantity'] == "50"


class CustomersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        customer = baker.make(Customer)
        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['first_name'] == customer.first_name
        assert data[0]['id'] == customer.id

    def test_create_customer(self):
        r = self.client.post('/api/customers/', {
            "first_name": "Иван",
            "last_name": "Иванов",
            "phone": "+79991234567"
        })
        new_id = r.json()['id']
        customers = Customer.objects.all()
        assert len(customers) == 1
        new_customer = Customer.objects.filter(id=new_id).first()
        assert new_customer.first_name == "Иван"

    def test_delete_customer(self):
        customers = baker.make(Customer, 10)
        assert len(Customer.objects.all()) == 10
        customer_id_to_delete = customers[3].id

        self.client.delete(f'/api/customers/{customer_id_to_delete}/')

        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 9
        assert customer_id_to_delete not in [i['id'] for i in data]

    def test_update_customer(self):
        customers = baker.make(Customer, 10)
        customer = customers[2]

        self.client.put(f'/api/customers/{customer.id}/', {
            "first_name": "Петр",
            "last_name": "Петров",
            "phone": "+79997654321"
        })

        r = self.client.get(f'/api/customers/{customer.id}/')
        data = r.json()
        assert data['first_name'] == "Петр"


class OrdersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        order = baker.make(Order)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['id'] == order.id

    def test_create_order(self):
        customer = baker.make(Customer)
        r = self.client.post('/api/orders/', {
            "customer": customer.id,
            "address": "ул. Пушкина, дом 2"
        })
        new_id = r.json()['id']
        orders = Order.objects.all()
        assert len(orders) == 1
        new_order = Order.objects.filter(id=new_id).first()
        assert new_order.address == "ул. Пушкина, дом 2"

    def test_delete_order(self):
        orders = baker.make(Order, 10)
        assert len(Order.objects.all()) == 10
        order_id_to_delete = orders[3].id

        self.client.delete(f'/api/orders/{order_id_to_delete}/')

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 9
        assert order_id_to_delete not in [i['id'] for i in data]

    def test_update_order(self):
        orders = baker.make(Order, 10)
        order = orders[2]

        self.client.put(f'/api/orders/{order.id}/', {
            "customer": order.customer.id,
            "address": "Новый адрес доставки"
        })

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['address'] == "Новый адрес доставки"


class OrderItemsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        item = baker.make(OrderItem)
        r = self.client.get('/api/order-items/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['id'] == item.id

    def test_create_order_item(self):
        order = baker.make(Order)
        product = baker.make(Product)
        r = self.client.post('/api/order-items/', {
            "order": order.id,
            "product": product.id,
            "count": "3"
        })
        new_id = r.json()['id']
        items = OrderItem.objects.all()
        assert len(items) == 1
        new_item = OrderItem.objects.filter(id=new_id).first()
        assert new_item.count == "3"

    def test_delete_order_item(self):
        items = baker.make(OrderItem, 10)
        assert len(OrderItem.objects.all()) == 10
        item_id_to_delete = items[3].id

        self.client.delete(f'/api/order-items/{item_id_to_delete}/')

        r = self.client.get('/api/order-items/')
        data = r.json()
        assert len(data) == 9
        assert item_id_to_delete not in [i['id'] for i in data]

    def test_update_order_item(self):
        items = baker.make(OrderItem, 10)
        item = items[2]

        self.client.put(f'/api/order-items/{item.id}/', {
            "order": item.order.id,
            "product": item.product.id,
            "count": "10"
        })

        r = self.client.get(f'/api/order-items/{item.id}/')
        data = r.json()
        assert data['count'] == "10"