# Generated by Django 4.2.2 on 2023-09-05 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_remove_extraditionrequest_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraditionrequest',
            name='address',
        ),
    ]