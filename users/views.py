from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login(request):
    if request.method == 'POST':  # это указывается в html шаблоне в параметре method
        form = UserLoginForm(data=request.POST)  # данные от пользователя приходят в request.POST
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:  # если пользователь есть в бд и если он активен
                auth.login(request, user)  # то мы его авторизуем
                return HttpResponseRedirect(reverse(
                    'products:products'))  # и перенаправляем на страницу products (вид: 'products:products' нужен, так как в urls я указал app_name='products')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # сохраняю в бд
            messages.success(request,
                             'Вы успешно зарегались')  # сообщение при успешной регистрации(автоматом добавляется в context)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required  # декоратор для автоматической проверки авторизован ли пользователь
def profile(request):
    user = request.user  # чтобы не писать везде request.user
    if request.method == 'POST':  # случай обновления данных пользователем
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserUpdateForm(instance=user)  # instance(сущность) с какой сущностью работаем
    baskets = Basket.objects.filter(user=user)
    total_quantity = 0
    total_sum = 0
    for basket in baskets:
        total_quantity += basket.quantity
        total_sum += basket.sum()  # метод sum() уже прописан в самом классе в моделс
    # total_quantity = sum(basket.quantity for basket in baskets) так можно сократить строки кода
    # total_sum = sum(basket.sum() for basket in baskets)
    context = {'form': form, 'title': 'Личный кабинет',
               'baskets': baskets,  # чтобы нам выдавалась корзина 1 пользователя, а не всех сразу
               'total_quantity': total_quantity,
               'total_sum': total_sum,
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))
