# Generated by Django 4.2.2 on 2023-07-22 19:58

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_subbottomcategory_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Barkod'),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=django_ckeditor_5.fields.CKEditor5Field(null=True, verbose_name='Detay'),
        ),
    ]