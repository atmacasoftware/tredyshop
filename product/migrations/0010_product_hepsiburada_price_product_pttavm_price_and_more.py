# Generated by Django 4.2.2 on 2023-07-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_images_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hepsiburada_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='Hepsiburada Fiyatı'),
        ),
        migrations.AddField(
            model_name='product',
            name='pttavm_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='PttAvm Fiyatı'),
        ),
        migrations.AddField(
            model_name='product',
            name='trendyol_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='Trendyol Fiyatı'),
        ),
    ]