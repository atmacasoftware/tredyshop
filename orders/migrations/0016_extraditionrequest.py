# Generated by Django 4.2.2 on 2023-09-05 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_rename_is_publis_trendyol_product_is_publish_trendyol'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('orders', '0015_preorder_cart_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraditionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extradition_type', models.CharField(choices=[('Arızalı geldi', 'Arızalı geldi'), ('Hasarlı geldi', 'Hasarlı geldi'), ('Farklı ürün geldi', 'Farklı ürün geldi'), ('Bedeni bana uygun değil', 'Bedeni bana uygun değil'), ('Almaktan vazgeçtim', 'Almaktan vazgeçtim'), ('Hatalı sipariş geldi', 'Hatalı sipariş geldi'), ('Diğer', 'Diğer')], max_length=255, null=True, verbose_name='İade Nedeni')),
                ('description', models.TextField(help_text='İade talebeinizin daha hızlı sonuçlanması için açıklama yazabilirsiniz.', verbose_name='Açıklama')),
                ('image', models.ImageField(blank=True, upload_to='img/iade/', verbose_name='İade Fotoğrafı')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeraddress', verbose_name='İadenin Reddi Durumunda GÖnderilecek Adres')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Ürün')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
            ],
        ),
    ]