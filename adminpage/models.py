from django.db import models

# Create your models here.

class IssuedInvoices(models.Model):

    YEAR = (
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )

    MONTH = (
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
        ("8","8"),
        ("9","9"),
        ("10","10"),
        ("11","11"),
        ("12","12"),
    )


    name = models.CharField(verbose_name="Ad/Soyad/Ünvan", max_length=500, null=True)
    tax_number = models.BigIntegerField(verbose_name="Vergi Numarası", null=True)
    tax_administration = models.CharField(max_length=255, verbose_name="Vergi Dairesi", null=True, blank=True)
    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KVD Oranı", null=True, blank=False)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    edited_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Fatura Düzenlenme Tarihi", null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "2) Kesilen Faturalar"
        verbose_name_plural = "2) Kesilen Faturalar"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"

class InvoicesReceived(models.Model):
    YEAR = (
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )

    MONTH = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    )

    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KVD Oranı", null=True, blank=False)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "3) Alınan Faturalar"
        verbose_name_plural = "3) Alınan Faturalar"
        ordering = ['created_at']
