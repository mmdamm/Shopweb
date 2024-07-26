from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

    path('product/', views.product_list, name='product_list'),
    path('product/<slug:category_slug>', views.product_list, name='product_by_category'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail')
]
