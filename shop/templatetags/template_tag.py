from django import template
from ..models import *
from django.db.models import Count
from ..views import *

register = template.Library()


@register.simple_tag()
def most_expensive():
    return Product.objects.all().order_by('-new_price')[:5]


@register.simple_tag()
def suggestions(category, id):
    product = Product.objects.filter(category=category).exclude(id=id)[:5]
    # name = products.name
    return (product)
