# Generated by Django 4.2.2 on 2023-08-29 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('orders', '0010_order_distance_selling_contract_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_contract', models.BooleanField(default=False, verbose_name='Sözleşme Onayı')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeraddress')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]