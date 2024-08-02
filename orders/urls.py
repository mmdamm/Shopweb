from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('create-order/', views.create_order, name='create_order'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_details/<int:id>', views.order_detail, name='order_detail'),
    path('pdf/<int:id>>', views.send_to_pdf, name='pdf'),
    path('reference/<int:id>', views.reference, name='reference'),
    path('apply-discount/',views.apply_discount, name='apply_discount'),
]
