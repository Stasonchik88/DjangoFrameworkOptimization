import random
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page, never_cache
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import ProductCategory, Product
from basketapp.models import Basket


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'все'
                }
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)
            
            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                'mainapp/includes/inc_products_list_content.html',
                context=content,
                request=request)
            return JsonResponse({'result': result})


# Create your views here.
def main(request):
    products = get_products()[:3]
    basket = get_basket(request.user)

    return render(request, 'mainapp/index.html', context={
        'title': 'Главная',
        'products': products,
        'basket': basket,
    })
    

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

        
def get_hot_product(category):
    products = get_products()
    return random.sample(list(products), 1)[0]
    
    
def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:4]
    return same_products


@never_cache
@cache_page(3600)
def products(request, pk=None):
    categories = ProductCategory.objects.all()
    category = {'name': 'все'}
    hot_product = Product.objects.all()[0]
    products = Product.objects.all()[1:5]
    basket = get_basket(request.user)
    links_menu = get_links_menu()

    if pk:
        if pk == '0':
            category = get_object_or_404(ProductCategory, pk=pk)
            products = get_products_orederd_by_price()
            hot_product = get_hot_product(category)
            products = get_same_products(hot_product)
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)
    
    return render(request, 'mainapp/products.html', context={
        'title': 'Продукты',
        'categories': categories,
        'category': category,
        'hot_product': hot_product,
        'products': products,
        'basket': basket,
    })


@never_cache
def product(request, pk):

    content = {
        'title': 'продукты', 
        'links_menu': get_links_menu(), 
        'product': get_product(pk),
        'basket': get_basket(request.user),
    }
	
    return render(request, 'mainapp/product.html', content)


def contact(request):
    if settings.LOW_CACHE:
        key = f'locations'
        locations = cache.get(key)
        if locations is None:
            # locations = load_from_json('contact__locations')
            cache.set(key, locations)
    else:
        pass
        # locations = load_from_json('contact__locations')

    return render(request, 'mainapp/contact.html', context={
        'title': 'Контакты',
    })

# def load_from_json(file_name):
#     with open(os.path.join(JSON_PATH, file_name + '.json'), 'r',\
#     errors='ignore') as infile:
#     return json.load(infile)
