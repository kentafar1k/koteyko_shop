from django.db import models
from users.models import User

# после создания новой модели и миграции не стоит забывать регистрировать её в admin.py
class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Product Categories"  # Как будет выглядеть в о множественном числе (в админке)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)  # типа колличество на складе
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)  # связь многие к одному, on_delete - параметр решающий что делать с продуктами,если удалиться вся категория(ProductCategory)

    def __str__(self):
        return f"{self.name} | {self.category.name}"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)  # мы щас не используем, но в будущем они будут важны, чтобы узнать когда добавился например объект
    modified_timestamp = models.DateTimeField(auto_now_add=True)  # auto_now_add те автоматически добавляются сами

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price