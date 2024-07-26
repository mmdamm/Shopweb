from django import forms
from django.forms import ModelForm
from .models import *


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField()


class OrderForm(forms.ModelForm):
    # first_name = forms.CharField()
    class Meta:
        model = Order

        fields = ['first_name','last_name', 'phone','address','postal_code','province','city']
