# Generated by Django 3.2.21 on 2023-11-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0037_hepsiburada'),
    ]

    operations = [
        migrations.AddField(
            model_name='hepsiburada',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Token'),
        ),
    ]