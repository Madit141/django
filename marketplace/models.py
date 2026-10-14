from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class ProductType(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.TextField("Название товара")
    quantity = models.PositiveIntegerField("Количество", default=0)
    category = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, verbose_name="Категория")
    image = models.ImageField("Картинка", null=True, upload_to="products")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    first_name = models.TextField("Имя")
    last_name = models.TextField("Фамилия")
    phone = models.TextField("Телефон")

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Покупатель")
    address = models.TextField("Адрес доставки")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Заказ {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    count = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self) -> str:
        return f"{self.product.name} ({self.count})"

class Profile(models.Model):
    class Role(models.IntegerChoices):
        UNDEFINED = 0
        CUSTOMER = 1
        SELLER = 2

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    role = models.IntegerField(choices=Role, default=Role.UNDEFINED)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return self.user.username if self.user else "no_user"

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance, role=Profile.Role.UNDEFINED)