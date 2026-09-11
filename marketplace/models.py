from django.db import models

class ProductType(models.Model):
    name = models.TextField("Навазние")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.TextField("Название товара")
    quantity = models.TextField("Количество")
    category = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, verbose_name="Категория")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
