from django import forms
from django.forms import ModelForm
from .models import *


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone','address','province', 'postal_code', 'city']
