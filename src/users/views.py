from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        if (request.POST.get('website') or '').strip():
            return redirect('register')
        email = (request.POST.get('email') or '').strip().lower()
        password1 = request.POST.get('password1') or ''
        password2 = request.POST.get('password2') or ''

        if not email:
            messages.error(request, 'Введите email.')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        if len(password1) < 8:
            messages.error(request, 'Пароль должен быть минимум 8 символов.')
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(
                request,
                'Пользователь с таким email уже существует. Попробуйте войти.'
            )
            return redirect('login')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1
        )

        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('home')

    return render(request, 'users/register.html')