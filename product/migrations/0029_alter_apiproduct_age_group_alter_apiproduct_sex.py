# Generated by Django 4.2.2 on 2023-09-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_apiproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiproduct',
            name='age_group',
            field=models.CharField(blank=True, choices=[('Bebek', 'Bebek'), ('Bebek&Çocuk', 'Bebek&Çocuk'), ('Çocuk', 'Çocuk'), ('Genç', 'Genç'), ('Yetişkin', 'Yetişkin')], max_length=50, null=True, verbose_name='Yaş Grubu'),
        ),
        migrations.AlterField(
            model_name='apiproduct',
            name='sex',
            field=models.CharField(blank=True, choices=[('Erkek', 'Erkek'), ('Kadın/Kız', 'Kadın/Kız'), ('Unisex', 'Unisex')], max_length=50, null=True, verbose_name='Cinsiyet'),
        ),
    ]