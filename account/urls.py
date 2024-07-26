from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('logout',views.log_out,name='logout')
]