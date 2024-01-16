from django.urls import path
from .views import home, QRCodeView

urlpatterns = [
    path('', home, name='home'),
    path('qr_code/', QRCodeView.as_view(), name='qrcode'),
]
