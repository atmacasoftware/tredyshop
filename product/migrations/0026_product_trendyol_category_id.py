# Generated by Django 4.2.2 on 2023-09-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_alter_product_stock_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='trendyol_category_id',
            field=models.BigIntegerField(null=True, verbose_name='Trendyol Kategori Numarası'),
        ),
    ]