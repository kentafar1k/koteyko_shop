from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from products.models import ProductCategory, Product, Basket


# Create your views here.

def index(request):
    context = {
        'title': 'magaz'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {'title': 'каталог', 'categories': ProductCategory.objects.all()}
    if category_id:  # пришёл ли айдишник категории, это для того чтобы работали категории
        product_list = Product.objects.filter(category_id=category_id)
    else:
        product_list = Product.objects.all()

    paginator = Paginator(product_list, 4)  # Показывать 4 продуктов на странице
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context.update({'products': page_obj})

    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)  # какой продукт мы хотим добавить
    baskets = Basket.objects.filter(user=request.user, product=product)  # список всех элементов корзины (но там всего 1 элемент)

    if not baskets.exists():  # если не существует
        Basket.objects.create(user=request.user, product=product,
                              quantity=1)  # объект только создан, поэтому колличество его 1
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()  # first() - берет первый элемент списка
        basket.quantity += 1
        basket.save()  # save() и create() выполняют одну и ту же функцию
        return HttpResponseRedirect(current_page)

@login_required
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
