from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import uuid
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.


@login_required
def home(request):
    context = {'books': models.Book.objects.all()}
    return render(request, 'home.html', context)


@never_cache
def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user_username = User.objects.filter(username=username)

            if not user_username.exists():
                messages.error(request, 'No account with this username found.')
                return redirect('/login/')

            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                return redirect('/home/')
            else:
                messages.error(request, 'Wrong credentials!')
                return redirect('/login/')

        else:
            messages.error(request, 'Please fill all fields.')
            return redirect('/login/')

    return render(request, 'login.html')

@never_cache
def signup(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if email and username and password:

            user_email = User.objects.filter(email=email)
            user_username = User.objects.filter(username=username)

            if user_email.exists() or user_username.exists():
                messages.error(request, 'Username or email already exists')
                return redirect('/signup/')

            hashed_pass = make_password(password)
            user = User.objects.create(
                username=username,
                email=email,
                password = hashed_pass
            )
            
            user.save()
            return redirect('/home/')
        else:
            messages.error(request, 'Please fill all fields.')
            return redirect('/signup/')

    return render(request, 'signup.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')


def get_book(request, slug):
    try:
        book = models.Book.objects.get(slug=slug)
        context = {'book': book}
        return render(request, 'book_detail.html', context)
    except Exception as e:
        print(e)
