from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
import requests
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.mail import EmailMessage
from ecommerce.settings import EMAIL_HOST_USER
from user_accounts.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.template.loader import get_template, render_to_string
from django.utils.http import urlsafe_base64_encode
# Create your views here.
from django.contrib.auth.tokens import default_token_generator

class UserRegistrationView(APIView):
    def post(self, request):
        email = request.POST.get('email', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        mobile = request.POST.get('mobile', None)
        password = request.POST.get('password', None)
        msg_password = request.POST.get('password', None)

        if password:
            if len(password) < 6:
                return Response({'msg': 'Şifre 6 haneden küçük olamaz.'})

        user = User.objects.filter(email=email)

        if len(user) > 0:
            return Response({'msg': 'Girilen e-posta adresine kayıtlı hesap mevcuttur.'})
        else:
            password = make_password(password)
            data = User.objects.create(email=email, first_name=first_name, last_name=last_name, mobile=mobile,
                                       password=password, is_customer=True, is_active=True, is_staff=False,
                                       is_superuser=False)
            data.save()

            current_site = get_current_site(request)
            from_email = EMAIL_HOST_USER
            mail_subject = "Lütfen hesabınızı aktif ediniz."
            message = render_to_string("frontend/acccounts/account_verification_email.html", {
                'user': data,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(data.id)),
                'token': default_token_generator.make_token(data),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg': 'Tebrikler hesabınız oluşturuldu. Hesabınızı aktif etmeniz için e-posta adresinize mail gönderdik. Keyifli alışverişler dileriz.'})
