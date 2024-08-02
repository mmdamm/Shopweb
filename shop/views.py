from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    print(category)
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


def save(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        save_p = ProductSave.objects.all()
        p = []
        for i in save_p:
            name = str(i.products)
            p += [name]
        if str(product) not in p:
            save_product = ProductSave.objects.create(user=request.user, products=product)
            save_product.save()
            return HttpResponse('با موفقیت ذخیره شد')
        else:
            return HttpResponse('شما قبلا این محصول به فهرست علاقه مندیتان اضافه کرده اید.')


def save_list(request):
    if request.user.is_authenticated:
        save = ProductSave.objects.all()
        return render(request, 'shop/save.html', {'save': save})
