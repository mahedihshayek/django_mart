from django.shortcuts import render
from store.models import Category
from store.models import Product 

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)[:12]
    return render(request, 'index.html', {'products': products, 'categories': categories})



