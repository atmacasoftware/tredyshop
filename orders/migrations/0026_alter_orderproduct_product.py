# Generated by Django 4.2.2 on 2023-09-13 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_alter_apiproduct_options_and_more'),
        ('orders', '0025_extraditionrequestresult_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.apiproduct', verbose_name='Ürün'),
        ),
    ]