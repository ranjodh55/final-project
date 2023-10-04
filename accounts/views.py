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
                return render(request, 'accounts/login.html', context={'username':username, 'password': password})


            if not user_username[0].profile.is_email_verified:
                messages.warning(request, 'Email not verified!')
                return render(request, 'accounts/login.html', context={'username':username, 'password': password})


            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, 'Wrong credentials!')
                return render(request, 'accounts/login.html', context={'username':username, 'password': password})


        else:
            messages.warning(request, 'Please fill all fields.')
            return render(request, 'accounts/login.html', context={'username':username, 'password': password})

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

        context = {'email':email, 'username':username, 'password':password}
        if check_pass(password) == 0:
            if email and username and password:

                user_email = User.objects.filter(email=email)
                user_username = User.objects.filter(username=username)

                if user_email.exists() or user_username.exists():
                    messages.warning(
                        request, 'Username or email already exists')
                    return render(request, 'accounts/signup.html', context=context)

                hashed_pass = make_password(password)
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=hashed_pass
                )

                user.save()
                messages.success(
                    request, 'An email has been sent to your mail.')
                return render(request, 'accounts/signup.html', context=context)
            else:
                messages.warning(request, 'Please fill all fields.')
                return render(request, 'accounts/signup.html', context=context)
        else:
            messages.warning(
                request, 'Password must be at least 8 characters long, have at least one uppercase, one lowecase and one special character')
            return render(request, 'accounts/signup.html', context=context)
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

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            quantity = int(quantity)
            available = book.available_quantity
            if available >= quantity:
                cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
                cart_item, created = CartItems.objects.get_or_create(cart=cart, book=book)
                if created:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.save()
                return redirect('/accounts/cart/')
            else:
                messages.warning(
                    request, 'You order quantity exceeds the available book quantity.')
                return redirect(f'/books/{book.slug}')
        else:
            messages.warning(
                    request, 'Please enter a valid book quantity.')
            return redirect(f'/books/{book.slug}')

    return redirect('/accounts/cart/')


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        context = {'cart': cart}
        return render(request, 'accounts/cart.html', context)
    except Exception as e:
        print(e)
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
        cart.delete()
        return redirect('/accounts/empty-cart/')
    except Exception as e:
        return redirect('/accounts/cart/')


def forgot_password(request):
    email = ''
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.get(email=email)

            forgot_token = str(uuid.uuid4())
            send_forgot_password_email(email, forgot_token)
            profile = Profile.objects.get(user=user)
            profile.forgot_token = forgot_token
            profile.save()
            messages.success(
                    request, 'A link to reset your password was sent to your email address.')
            context = {'email':email}
        return render(request, 'accounts/forgot.html',context)

    except Exception as e:
        messages.warning(request,'No user exists with this email address.')
        context = {'email':email}

        return render(request, 'accounts/forgot.html',context)


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
def place_order(request):
    try:
        if request.method == 'POST':
            
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_id = key.split('_')[1]  # Extract the cart item ID from the field name
                    quantity = value

                    # Retrieve the cart item
                    cart_item = CartItems.objects.get(id=cart_item_id)

                    # Update the cart item's quantity
                    cart_item.quantity = quantity
                    cart_item.save()
            cart_id = request.POST.get('cart_id')
            cart = Cart.objects.get(id = cart_id)
            context = {'cart':cart}
            return render(request,'accounts/order.html',context)
    except Exception as e:
            print(e)
            return redirect('/accounts/cart/')


# def order(request):
#     return render(request, 'accounts/')

@login_required
def order(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        if request.method == 'POST':
            for cart_item in cart.cart_items.all():
                cart_item.book.available_quantity -= cart_item.quantity
                cart_item.book.save()
            cart.is_paid = True
            cart.save()
            messages.success(request, 'Order placed sucessfully.')
            return redirect('/accounts/empty-cart/')
    except Exception as e:
        messages.warning(request, 'No Items in your cart.')
        print(e)
        return redirect('/accounts/place_order/')
    


@login_required
def cart_is_empty(request):
    return render(request, 'accounts/empty_cart.html')


@login_required
def profile(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if username or email or password:
            username_ne = username != request.user.username
            email_ne = email != request.user.email
            if username_ne or email_ne or password:
                user = User.objects.get(username= request.user.username)
                if username_ne and username:
                    user.username = username
                if password:
                    if check_pass(password) == 0:
                        hashed_pass = make_password(password)
                        user.password = hashed_pass
                    else:
                        messages.warning(request, 'Password must be at least 8 characters long, have at least one uppercase, one lowecase and one special character.')
                        return redirect('/accounts/profile/')  
                if email and email_ne:
                    print(email)
                    user.email = email
                    profile = Profile.objects.get(user=user)
                    profile.is_email_verified = False
                    profile.save()
                    user.save()
                    messages.warning(request, 'Email was changed, you need to verify your new email first.')
                    logout(request)
                    return redirect('/')
                user.save()
                print(user.email)
                messages.success(request, 'Updated profile successfully.')
                return redirect('/accounts/profile/')  
    return render(request, 'accounts/profile.html')