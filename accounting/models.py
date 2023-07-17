from django.db import models

# Create your models here.

class ExpensesIncurred(models.Model):
    STATUS = (
        ("Ödenecek", "Ödenecek"),
        ("Ödendi", "Ödendi"),
    )
    name = models.CharField(max_length=500, verbose_name="Ödeme Adı", null=True, blank=False)
    company = models.CharField(max_length=500, verbose_name="Ödeme Yapılan Yer", null=True, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Ödeme Tutarı", null=True, blank=False)
    status = models.CharField(choices=STATUS, max_length=20, null=True, blank=True, verbose_name="Ödeme Durumu")
    image = models.ImageField(upload_to="img/accounting/", verbose_name="Fatura", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "1) Yapılan Ödemeler"
        verbose_name_plural = "1) Yapılan Ödemeler"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"

