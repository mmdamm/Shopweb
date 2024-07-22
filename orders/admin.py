from django.contrib import admin
from .models import *
import openpyxl
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect


# Register your models here.
def export_to_excel(modelAdmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
    wb = openpyxl.Workbook()
    wa = wb.active
    wa.title = 'Orders'
    columns = ['ID', 'First Name', 'Last Name', 'Phone', 'Address', 'Postal Code',
               'Province', 'City', 'Paid', 'Created']
    wa.append(columns)
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        wa.append([
            order.id, order.first_name, order.last_name, order.phone, order.address,
            order.postal_code, order.province, order.city, order.paid, created
        ])
    wb.save(response)
    return response


export_to_excel.short_description = 'Export to Excel'


class OderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'first_name', 'last_name', 'paid', 'status_order']
    list_filter = ['status_order', 'paid']
    inlines = [OderItemInline]
    actions = [export_to_excel]
    list_editable = ['status_order']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        t = Order.STATUS_CHOISES
        if form.changed_data == ['status_order']:
            for i in range(8):
                if t[i][0] == obj.status_order:
                    # send_sms_normal(t[i][1])
                    messages.success(request, f'"{t[i][1]}" sent to customer')

