from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from cart.models import Cart, CartItem
from store.models import Category

from django.contrib import messages


def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart')
    categories = Category.objects.all()
    context = {
        'categories':categories,
        'form': form,
    }
    return render(request, 'accounts/register.html',  context)

def profile(request):
    categories = Category.objects.all()
    return render(request, 'accounts/dashboard.html', { 'categories': categories})

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        

        if user is not None:
            login(request, user)
            session_key = get_create_session(request)
            cart, created = Cart.objects.get_or_create(cart_id=session_key)
            if created:
                cart.user = user
                cart.save()
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(cart=cart)
                for item in cart_item:
                    item.user = user
                    item.save()
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }    
    return render(request, 'accounts/signin.html',context)

def user_logout(request):
    logout(request)
    return redirect('login')