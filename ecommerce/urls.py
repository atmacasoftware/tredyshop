"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('waiting/', include('waitingdeploy.urls')),
    path('', include('product.urls')),
    path('', include('mainpage.urls')),
    path('', include('store.urls')),
    path('', include('customer.urls')),
    path('', include('carts.urls')),
    path('', include('orders.urls')),

    path('accounts/', include('allauth.urls')),

    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.png')),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="frontend/acccounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="frontend/acccounts/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="frontend/acccounts/set_password.html"),
         name="password_reset_confirm"),
    path('reset_password_complate/',
         auth_views.PasswordResetCompleteView.as_view(template_name="frontend/acccounts/reset_password_complate.html"),
         name="password_reset_complete"),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
