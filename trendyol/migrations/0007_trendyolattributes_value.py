# Generated by Django 3.2.21 on 2024-03-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0006_alter_trendyolattributes_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='trendyolattributes',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Özellik Değeri'),
        ),
    ]
