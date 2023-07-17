from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime, timezone
from categorymodel.models import MainCategory
from mainpage.models import City, County
from user_accounts.models import User


# Create your models here.

class CustomerAddress(models.Model):
    BILL_TYPE = (
        ('Bireysel', "Bireysel"),
        ('Kurumsal', "Kurumsal"),
    )

    CURRENT_ADDRES = (
        ("Evet", "Evet"),
        ("Hayır", "Hayır"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    title = models.CharField(max_length=100, verbose_name="Adres Başlık", blank=False, null=True)
    first_name = models.CharField(verbose_name="Ad", max_length=50, null=True, blank=False)
    last_name = models.CharField(verbose_name="Soyad", max_length=50, null=True, blank=False)
    mobile = models.CharField(max_length=50, verbose_name="Telefon Numarası", null=True, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Şehir")
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True, blank=False, verbose_name="İlçe")
    neighbourhood = models.CharField(max_length=100, verbose_name="Mahalle", null=True, blank=False)
    address = models.TextField(max_length=1000, verbose_name="Adres Detay", null=True, blank=False)
    bill_type = models.CharField(choices=BILL_TYPE, blank=False, null=True, max_length=20, verbose_name="Fatura Tipi")
    tc = models.CharField(null=True, blank=True, max_length=11, verbose_name="T.C. Kimlik Numarası")
    company_name = models.CharField(verbose_name="Şirket Adı", max_length=255, null=True, blank=True)
    tax_number = models.CharField(null=True, blank=True, max_length=10, verbose_name="Vergi Numarası")
    tax_administration = models.CharField(null=True, blank=True, verbose_name="Vergi Dairesi", max_length=255)
    is_active = models.CharField(choices=CURRENT_ADDRES, max_length=20, null=True, blank=True, default="Hayır",
                                 verbose_name="Geçerli Adres Yap")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "1) Müşteri Adresleri"
        verbose_name_plural = "1) Müşteri Adresleri"

    def __str__(self):
        return f"{self.title}"

class Subscription(models.Model):
    email = models.EmailField(max_length=300, verbose_name="Email Adresi", null=True, blank=False)
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "2) Abonelikler"
        verbose_name_plural = "2) Abonelikler"

    def __str__(self):
        return f"{str(self.email)}"

class Bonuses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Müşteri")
    bonuses = models.FloatField(verbose_name="Bonus")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "3) Müşteri Bonusları"
        verbose_name_plural = "3) Müşteri Bonusları"

    def __str__(self):
        return f"{str(self.user.get_full_name())}"


class Coupon(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name="Müşteri")
    coupon_code = models.CharField(max_length=50, verbose_name="Kupon Kodu", null=True)
    coupon_price = models.FloatField(verbose_name="Kupon Fiyatı", null=True)
    coupon_conditional = models.BigIntegerField(verbose_name="Kupon Şartı")
    coupon_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name="İlgili Kategori")
    is_active = models.BooleanField(default=False, null=True, verbose_name="Kullanımda mı?")
    start_date = models.DateField(null=True, verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(null=True, verbose_name="Bitiş Tarihi")
    is_completed = models.BooleanField(default=False, null=True, verbose_name="Süresi bitti mi?")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "4) Müşteri Kuponları"
        verbose_name_plural = "4) Müşteri Kuponları"

    def __str__(self):
        return f"{str(self.coupon_code)}"

    def completed(self):
        import math
        gecen_gun = (self.end_date - datetime.now().date()).days

        if gecen_gun >= 0:
            self.is_completed = True
            self.save()
