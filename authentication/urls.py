from django.urls import path
from . import views

urlpatterns = [
    path('',views.register, name='register'),
    path('verfication/',views.verify_otp, name='verfication'),
    path('resend-otp/',views.resend_otp, name='resendotp')
]
