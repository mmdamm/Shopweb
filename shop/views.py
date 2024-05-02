from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    category = product.category
    # request.session.delete()
    context = {
        'product': product,
        'category': category,
    }
    return render(request, 'shop/detail.html', context)
