from django import template
from ..models import *
from django.db.models import Count
from ..views import *

register = template.Library()


@register.inclusion_tag("shop/list2.html")
def most_expensive(count=6):
    exp_product = Product.objects.all().order_by('-new_price')[:count]
    context = {
        'exp_product': exp_product
    }
    print(exp_product)
    return context

@register.simple_tag()
def most_expensive(count=6):
    return Product.objects.all().order_by('-new_price')[:count]

