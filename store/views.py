# from django.shortcuts import render,get_object_or_404
# from .models import Product
# from category.models import Category
# from django.core.paginator import Paginator


# from django.db.models import Q
# # Create your views here.

# def store(request, category_slug=None):
#     if category_slug:
#         category = get_object_or_404(Category, slug = category_slug)
#         products = Product.objects.filter(is_available=True,category = category)
#         page = request.GET.get('page')
#         paginator = Paginator(products, 3) # pagination - product per page
#         paged_product = paginator.get_page(page)
#     else:
#         products = Product.objects.filter(is_available=True)
#         page = request.GET.get('page')
#         paginator = Paginator(products, 3)     
#         paged_product = paginator.get_page(page)
#         for i in paged_product:
#             print(i)
#         print(paged_product.has_next(), paged_product.has_previous(), paged_product.previous_page_number, paged_product.next_page_number)              
#     categories = Category.objects.all()
#     context = {'products':paged_product,'categories':categories,}
#     return render(request, 'store/store.html',context)


# def search(request):
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
#         if keyword:
#             products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
#             product_count = products.count()
#     context = {
#         'products': products,
#         'p_count': product_count,
#     }
#     return render(request, 'store/store.html', context)


# def product_detail(request,category_slug, product_slug):
#     single_product = Product.objects.get(slug = product_slug, category__slug = category_slug)
#     # print('single product ', single_product)
    
#     return render(request, 'store/product-detail.html', {'product' : single_product})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from cart.models import CartItem
from django.db.models import Q

from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct



def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        product_count = products.count()
    categories = Category.objects.all()
    context = {
        'categories':categories,
        'products': paged_products,
        'p_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    categories = Category.objects.all()   
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'categories':categories,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    categories = Category.objects.all()        
    context = {
        'categories':categories,
        'products': products,
        'p_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Review has been updated successfully.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Review has been submitted successfully.')
                return redirect(url)