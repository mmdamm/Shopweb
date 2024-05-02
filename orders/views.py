from django.shortcuts import render,redirect
from .forms import *
from account.models import ShopUser
import random
from django.contrib import messages
from cart.common.sms import send_sms_with_template,send_sms_normal
# Create your views here.

def verify_code(request):
    pass


def verify_phone(request):
    print('------------------------------------14')
    if request.method=='POST':
        print('------------------------------------16')
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            print('------------------------------------17')
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registered.')
                print('------------------------------------18')
                return redirect('orders:verify_phone')

            else:
                print('------------------------------------19')
                tokens = {'token': ''.join(random.choices('0123456789', k=4))}
                request.session['verify_code'] = tokens['token']
                request.session['phone'] = phone
                print(tokens)
                send_sms_normal('09944326389')
                send_sms_with_template(phone, tokens, 'mmdshop')

                messages.error(request, 'verify code sent successfully')
                return redirect('orders:verify_code')
    else:
        form = PhoneVerificationForm()

    return render(request, 'verify-code.html', {'form': form})

