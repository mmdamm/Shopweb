from django.shortcuts import render, redirect
from .forms import *
from account.models import ShopUser
import random
from django.http import HttpResponse
from django.contrib import messages
from cart.common.sms import send_sms_with_template, send_sms_normal
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
from cart.cart import Cart
from django.http import HttpResponse
import requests
import json
from django.conf import settings
from orders.models import *
import time
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                user = authenticate(request, username=phone,
                                    password=request.POST['password'])
                login(request,user)
                messages.error(request, 'this phone is already registered.')
                return redirect("orders:create_order")

            else:
                tokens = {'token': ''.join(random.choices('0123456789', k=4))}
                time1 = time.time()
                request.session['verification_code'] = tokens['token']
                request.session['phone'] = phone
                request.session['time1'] = time1
                request.session['password']=request.POST.get('password')
                print(tokens)
                send_sms_normal()
                messages.error(request, 'verification code sent successfully.')
                return redirect('orders:verify_code', )
    elif request.user.is_authenticated:
        return redirect('orders:create_order')
    else:
        form = PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        time2 = time.time()
        time1 = request.session['time1']
        if time2 - time1 < 30:
            code = request.POST.get('code')
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = ShopUser.objects.create_user(phone)
                user.set_password(request.session['password'])
                # muss send sms to user
                user.save()
                # print(user)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']

                return redirect('orders:create_order')

            else:
                messages.error(request, 'verification code is wrong')
        else:
            messages.error(request, 'verificationg')
            redirect('orders:verify_phone')
    return render(request, 'verify_code.html')


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        # form.first_name(initial='11')

        # form_name = OrderForm.first_name(initial=request.user)
        if form.is_valid:

            order = form.save()
            order.buyer = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'],
                                         weight=item['weight'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:request')

    else:
        form = OrderForm()
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'create_order.html', context)


#
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


def send_request(request):
    order = Order.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.items.all():
        description += item.product.name + ", "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(request):
    order = Order.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']

            if response_json['Status'] == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.save()
                return render(request, 'payment-tracking.html',
                              {"success": True, 'RefID': reference_id, "order_id": order.id})
            else:
                return render(request, 'payment-tracking.html',
                              {"success": False, })
        del request.session['order_id']
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def order_list(request):
    user = request.user
    order = Order.objects.filter(buyer=user)
    return render(request, 'order_list.html', {'order': order})


@login_required
def order_detail(request, id):
    user = request.user
    order = Order.objects.get(id=id)
    if user == order.buyer:

        try:
            status = order.status_order[1]
            show_status = list(map(lambda x: Order.STATUS_CHOICES[int(order.status_order[1])][1], Order.STATUS_CHOICES))
            context = {
                'order': order,
                'status': show_status[1]
            }
            return render(request, 'order_detail.html', context)
        except:
            return HttpResponse('NOT FOUND')
    else:
        return HttpResponse('This URL is not related to this user.')
