# Generated by Django 3.2.21 on 2023-10-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0042_binlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='preorder',
            name='order_number',
            field=models.CharField(max_length=255, null=True, verbose_name='Sipariş Numarası'),
        ),
    ]