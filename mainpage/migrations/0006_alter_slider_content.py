# Generated by Django 4.2.2 on 2023-07-22 16:53

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_alter_slider_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(null=True, verbose_name='Text'),
        ),
    ]