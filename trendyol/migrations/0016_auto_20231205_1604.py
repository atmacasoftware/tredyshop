# Generated by Django 3.2.21 on 2023-12-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0015_trendyolmoreproductorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trendyolmoreproductorder',
            name='orders',
        ),
        migrations.AddField(
            model_name='trendyolmoreproductorder',
            name='order_number',
            field=models.CharField(max_length=255, null=True, verbose_name='Sipariş Numarası'),
        ),
        migrations.AddField(
            model_name='trendyolmoreproductorder',
            name='packet_number',
            field=models.CharField(max_length=255, null=True, verbose_name='Paket Numarası'),
        ),
    ]