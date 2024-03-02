from django.shortcuts import render
from shop.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.


@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        cart.add()
        cart.save()
        print(cart)
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
        }
        return JsonResponse(context)

    except:
        return JsonResponse({"error": "Invalid request."})


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart/detail.html', context)
