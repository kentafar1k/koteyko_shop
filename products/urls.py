from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category_id>', views.products, name='category'),
    path('products/', views.products, name='products'),
    path('test-context/', views.test_context, name='test_context'),
    path('basket-add/<int:product_id>', views.basket_add, name='basket_add'),  # <int:...> должен совпадать с тем, что мы передаём в контроллере(вьюхе)
    path('basket-delete/<int:id>', views.basket_delete, name='basket_delete'),
]