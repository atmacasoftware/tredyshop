# Generated by Django 4.2.2 on 2023-09-05 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_rename_is_publis_trendyol_product_is_publish_trendyol'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0016_extraditionrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraditionrequest',
            name='product',
        ),
        migrations.AddField(
            model_name='extraditionrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AddField(
            model_name='extraditionrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.CreateModel(
            name='ExtraditionRequestProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Güncellenme Tarihi')),
                ('extraditionrequest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.extraditionrequest', verbose_name='Sipariş')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Ürün')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
            ],
        ),
    ]