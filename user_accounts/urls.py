from django.urls import path
from user_accounts.views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('user/register/api/', UserRegistrationView.as_view(), name="register_api"),
]
