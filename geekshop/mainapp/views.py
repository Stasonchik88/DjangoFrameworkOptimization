import random
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket

# Create your views here.
def main(request):
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
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
    products = Product.objects.filter(category=category)

    return random.sample(list(products), 1)[0]
    
    
def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:4]

    return same_products


def products(request, pk=None):
    categories = ProductCategory.objects.all()
    category = {'name': 'все'}
    hot_product = Product.objects.all()[0]
    products = Product.objects.all()[1:5]
    basket = get_basket(request.user)
    
    if pk is not None and pk != 0:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category__pk=pk).order_by('price')
        hot_product = get_hot_product(category)
        products = get_same_products(hot_product)
    
    return render(request, 'mainapp/products.html', context={
        'title': 'Продукты',
        'categories': categories,
        'category': category,
        'hot_product': hot_product,
        'products': products,
        'basket': basket,
    })


def product(request, pk):

    content = {
        'title': 'продукты', 
        'links_menu': ProductCategory.objects.all(), 
        'product': get_object_or_404(Product, pk=pk), 
        'basket': get_basket(request.user),
    }
	
    return render(request, 'mainapp/product.html', content)


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title': 'Контакты',
    })

# def load_from_json(file_name):
#     with open(os.path.join(JSON_PATH, file_name + '.json'), 'r',\
#     errors='ignore') as infile:
#     return json.load(infile)
