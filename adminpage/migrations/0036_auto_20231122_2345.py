# Generated by Django 3.2.21 on 2023-11-22 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0035_alter_harcamalar_harcama_tipi'),
    ]

    operations = [
        migrations.AddField(
            model_name='izinler',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AddField(
            model_name='izinler',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Güncellenme Tarihi'),
        ),
    ]