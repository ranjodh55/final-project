from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import uuid
from . import models
from .models import Profile
from django.contrib.auth.decorators import login_required
from accounts.models import Cart, CartItems
from books.models import Book


# Create your views here.


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user_username = User.objects.filter(username=username)

            if not user_username.exists():
                messages.error(request, 'No account with this username found.')
                return redirect('/accounts/login/')

            if not user_username[0].profile.is_email_verified:
                messages.error(request, 'Email not verified!')
                return redirect('/accounts/login/')

            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('/')
            else:
                messages.error(request, 'Wrong credentials!')
                return redirect('/accounts/login/')

        else:
            messages.error(request, 'Please fill all fields.')
            return redirect('/accounts/login/')

    return render(request, 'accounts/login.html')


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
                return redirect('/accounts/signup/')

            hashed_pass = make_password(password)
            user = User.objects.create(
                username=username,
                email=email,
                password=hashed_pass
            )

            user.save()
            messages.warning(request, 'An email has been sent to your mail.')
            return redirect('/accounts/signup/')
        else:
            messages.error(request, 'Please fill all fields.')
            return redirect('/accounts/signup/')

    return render(request, 'accounts/signup.html')


def activate_email(request, email_token):

    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid email token.')


def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def add_to_cart(request, id):
    book = Book.objects.get(id=id)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(cart=cart, book=book)
    cart_items.save()
    return redirect(f'/books/{book.slug}')


@login_required
def cart(request):
    context = {'cart': Cart.objects.get(is_paid=False, user=request.user)}
    return render(request, 'accounts/cart.html', context)


@login_required
def remove_from_cart(request, cart_item_id):
    try: 
        cart_item = CartItems.objects.get(id = cart_item_id)
        cart_item.delete()
        return redirect('/accounts/cart/')
    except Exception as e: 
        return redirect('/accounts/cart/')
