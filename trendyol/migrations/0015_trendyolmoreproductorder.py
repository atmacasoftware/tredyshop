# Generated by Django 3.2.21 on 2023-12-05 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0014_trendyolorders_is_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendyolMoreProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField(null=True, verbose_name='Adet')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Ürün Adı')),
                ('barcode', models.CharField(max_length=100, null=True, verbose_name='Barkod')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='Renk')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Beden')),
                ('stock_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Stok Kodu')),
                ('unit_price', models.FloatField(null=True, verbose_name='Birim Fiyat')),
                ('sales_amount', models.FloatField(null=True, verbose_name='Satış Tutarı')),
                ('discount_amount', models.FloatField(blank=True, null=True, verbose_name='İndirim Tutarı')),
                ('orders', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trendyol.trendyolorders', verbose_name='Trendyol Siparişi')),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
    ]