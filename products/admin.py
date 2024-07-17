from django.contrib import admin
from products.models import ProductCategory, Product, Basket

# Register your models here.
# login: andre pass: 6823

admin.site.register(ProductCategory)

admin.site.register(Basket)


@admin.register(Product)  # обязательная регистрация
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')  # передаём переменные, которые хотим видеть в таблице админки
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category')  # можно по приколу объединить некоторые поля
    readonly_fields = ('short_description',)  # типа теперь нельзя редактировать
    ordering = ('name',)  # распорядок от а до я
    search_fields = ('name',)  # по какому параметру работает поиск


class BasketAdminInline(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    # extra = 0  # типа нужны ли доп строки для добавления продуктов (по умолчанию 1)
