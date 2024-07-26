from django.shortcuts import render
from django.contrib.auth import logout
# Create your views here.


def log_out(request):
    user=request.user
    logout(request)
    return render(request,'log_out.html',{'user':user})
