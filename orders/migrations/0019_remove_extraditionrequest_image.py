# Generated by Django 4.2.2 on 2023-09-05 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_remove_extraditionrequest_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraditionrequest',
            name='image',
        ),
    ]