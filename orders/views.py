from django.shortcuts import render,redirect
from .forms import *
from account.models import ShopUser
import random
from django.http import HttpResponse
from django.contrib import messages
from cart.common.sms import send_sms_with_template,send_sms_normal
# Create your views here.



def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registered.')
                return redirect('orders:verify_phone')
            else:
                tokens = {'token': ''.join(random.choices('0123456789', k=4))}
                request.session['verification_code'] = tokens['token']
                request.session['phone'] = phone
                print(tokens)
                send_sms_normal()
                messages.error(request, 'verification code sent successfully.')
                return HttpResponse(f'success{tokens}',{"form": form})
    else:
        form = PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form': form})


def verify_code(request):
    pass

