from django.contrib import admin
from .models import *


# Register your models here.

class OderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'first_name', 'last_name', 'paid']
    list_filter = ['id', 'paid', 'last_name']
    inlines = [OderItemInline]
