# Generated by Django 3.2.21 on 2024-03-02 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_code',
        ),
    ]
