# Generated by Django 4.2.2 on 2023-07-19 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Kategori Adı')),
                ('keyword', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='img/category/')),
                ('order', models.IntegerField(null=True, verbose_name='Sırası')),
                ('is_active', models.BooleanField(default=True, verbose_name='Yayınlansın mı?')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': '1) Ana Kategoriler',
                'verbose_name_plural': '1) Ana Kategoriler',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Kategori Adı')),
                ('keyword', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='img/category/')),
                ('is_active', models.BooleanField(default=True, verbose_name='Yayınlansın mı?')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('maincategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categorymodel.maincategory', verbose_name='Ana Kategori')),
            ],
            options={
                'verbose_name': '2) Alt Kategoriler',
                'verbose_name_plural': '2) Alt Kategoriler',
            },
        ),
    ]