from django.urls import path
from .views import home, qr_code_view

urlpatterns = [
    path('', home, name='home'),
    path('qr_code/', qr_code_view, name='qrcode'),
]

