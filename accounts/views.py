from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import login, logout
import uuid
from . import models
from .models import Profile
from django.contrib.auth.decorators import login_required
from accounts.models import Cart, CartItems
from books.models import Book
from base.emails import send_forgot_password_email
import re

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user_username = User.objects.filter(username=username)

            if not user_username.exists():
                messages.warning(
                    request, 'No account with this username found.')
                return redirect('/accounts/login/')

            if not user_username[0].profile.is_email_verified:
                messages.warning(request, 'Email not verified!')
                return redirect('/accounts/login/')

            user = User.objects.get(username=username)
            print(check_password(password, user.password))
            print(user.password)
            if check_password(password, user.password):
                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('/')
            else:
                messages.warning(request, 'Wrong credentials!')
                return redirect('/accounts/login/')

        else:
            messages.warning(request, 'Please fill all fields.')
            return redirect('/accounts/login/')

    return render(request, 'accounts/login.html')

def check_pass(password):
    flag = 0
    while True:
        if (len(password)<=8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]" , password):
            flag = -1
            break
        elif re.search("\s" , password):
            flag = -1
            break
        else:
            flag = 0
            print("Valid Password")
            break
    return flag
    

def signup(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if check_pass(password) == 0:
            if email and username and password:

                user_email = User.objects.filter(email=email)
                user_username = User.objects.filter(username=username)

                if user_email.exists() or user_username.exists():
                    messages.warning(
                        request, 'Username or email already exists')
                    return redirect('/accounts/signup/')

                hashed_pass = make_password(password)
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=hashed_pass
                )

                user.save()
                messages.success(
                    request, 'An email has been sent to your mail.')
                return redirect('/accounts/signup/')
            else:
                messages.warning(request, 'Please fill all fields.')
                return redirect('/accounts/signup/')
        else:
            messages.warning(
                request, 'Password must be at least 8 characters long, have at least one uppercase, one lowecase and one special character')
            return redirect('/accounts/signup/')
    return render(request, 'accounts/signup.html')


def activate_email(request, email_token):

    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email verified successfully. You can log in.')
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

    if request.method == 'POST':
        print('post')
        quantity = int(request.POST.get('quantity'))
        available = book.available_quantity
        if available >= quantity:
            print(available)
            print('quantity',quantity)
            cart_item = CartItems.objects.create(cart=cart, book=book)
            cart_item.quantity = quantity
            cart_item.save()
            return redirect('/accounts/cart/')
        else:
            messages.warning(
                request, 'You order quantity exceeds the available book quantity.')
            return redirect(f'/books/{book.slug}')

    return redirect('/accounts/cart/')


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        context = {'cart': cart}
        return render(request, 'accounts/cart.html', context)
    except Exception as e:
        return redirect('/accounts/empty-cart/')


@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItems.objects.get(id=cart_item_id)
        cart_item.delete()
        return redirect('/accounts/cart/')
    except Exception as e:
        return redirect('/accounts/cart/')


@login_required
def remove_all_from_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        print(cart)
        cart.cart_items.all().delete()
        return redirect('/accounts/empty-cart/')
    except Exception as e:
        return redirect('/accounts/cart/')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)

        if user:
            forgot_token = str(uuid.uuid4())
            send_forgot_password_email(email, forgot_token)
            profile = Profile.objects.get(user=user)
            profile.forgot_token = forgot_token
            profile.save()
            messages.success(
                request, 'A link to reset your password was sent to your email address.')
            return redirect('/accounts/forgot')

        else:
            messages.warning('No user exists with this email address.')
            return redirect('/accounts/forgot')
    return render(request, 'accounts/forgot.html')


def reset_pass(request, forgot_token):
    try:
        if request.method == 'POST':
            user = Profile.objects.get(forgot_token=forgot_token)
            if user:
                password = request.POST.get('password')
                if password:
                    if check_pass(password) == 0:
                        hashed_pass = make_password(password)
                        user.user.password = hashed_pass
                        user.user.save()
                        messages.success(
                            request, 'Your password was reset successfully.')
                        return redirect('/accounts/login')
                    else:
                        messages.warning(
                            request, 'Password must be at least 8 characters long, have at least one uppercase, one lowecase and one special character.')
                        return redirect('/accounts/login')
        return render(request, 'accounts/reset.html')
    except Exception as e:
        return HttpResponse('Invalid Token')


@login_required
def order(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        if request.method == 'POST':
            order = int(request.POST.get('quantity'))
            for cart_item in cart.cart_items.all():
                available = cart_item.book.available_quantity
                # order = cart_item.quantity
                if available >= order:
                    cart_item.book.available_quantity -= order
                    cart_item.book.save()
                    cart.is_paid = True
                    cart.save()
                    messages.success(request, 'Order placed sucessfully.')
                    return redirect('/accounts/empty-cart/')
                else:
                    messages.warning(
                        request, 'You order quantity exceeds the available book quantity.')
                    return redirect('/accounts/cart/')
    except Exception as e:
        messages.warning(request, 'No Items in your cart.')
        print(e)
        return redirect('/accounts/cart/')
    return render('accounts/cart.html')


@login_required
def cart_is_empty(request):
    return render(request, 'accounts/empty_cart.html')


@login_required
def decrease(request, quantity):
    try:
        if quantity > 1:
            return quantity-1
    except Exception as e:
        return HttpResponse(e)


@login_required
def profile(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if username or email or password:
            if username != request.user.username and email != request.user.email:
                user = User.objects.get(username= username)
                if username:
                    user.username = username
                if password:
                    if check_pass(password) == 0:
                        hashed_pass = make_password(password)
                        user.password = hashed_pass
                    else:
                        messages.warning(request, 'Password must be at least 8 characters long, have at least one uppercase, one lowecase and one special character.')
                        return redirect('/accounts/profile/')  
                user.save()
                messages.success(request, 'Updated profile successfully.')
    return render(request, 'accounts/profile.html')