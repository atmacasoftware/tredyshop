# Generated by Django 3.2.21 on 2024-03-24 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20240316_1301'),
        ('trendyol', '0014_auto_20240324_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trendyolreportproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productvariant', verbose_name='Ürünler'),
        ),
    ]