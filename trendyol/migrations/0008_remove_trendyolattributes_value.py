# Generated by Django 3.2.21 on 2024-03-23 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0007_trendyolattributes_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trendyolattributes',
            name='value',
        ),
    ]