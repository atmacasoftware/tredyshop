# Generated by Django 4.2.2 on 2023-09-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_alter_apiproduct_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiproduct',
            name='is_active',
            field=models.CharField(choices=[('Evet', 'Evet'), ('Hayir', 'Hayir')], default='Aktif', max_length=50, null=True, verbose_name='Mevcut mu?'),
        ),
    ]