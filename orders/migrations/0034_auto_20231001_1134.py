# Generated by Django 3.2.21 on 2023-10-01 08:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_auto_20231001_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preorder',
            name='distance_selling_contract',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Mesafeli Satış Sözleşmesi'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='preliminary_information_form',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Ön Bilgilendirme Formu'),
        ),
    ]