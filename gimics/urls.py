from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('qr_code/', QRCodeView.as_view(), name='qrcode'),
]
