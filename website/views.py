from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from service.forms import LoginForm, PasswordChangeForm, RegisterForm


def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                messages.success(request, 'Jūs sėkmingai prisijungėte')
                return redirect('home')

            else:
                messages.error(request, "Neteisingai suvesi duomenys")
                return redirect('login')
    return render(request, 'service/login.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('naujas slaptažodis'))
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Slaptažodis sękmingai paskeistas')
            return redirect('login')
        else:
            return render(request, 'service/password_changed.html', {'form': form})

    return render(request, 'service/password_changed.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Jūs sėkmingai atsijungėte!")
    return redirect("home")


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'service/register.html', {'form': form})
