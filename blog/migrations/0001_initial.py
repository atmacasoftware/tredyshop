# Generated by Django 3.2.21 on 2024-01-07 02:01

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='static/img/blog/', verbose_name='Blog Resmi')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Başlık')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('blog_views', models.IntegerField(blank=True, default=0, null=True)),
                ('is_publish', models.BooleanField(default=False, verbose_name='Yayında mı?')),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=1000, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Blog Kategorisi')),
                ('slug', models.SlugField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRatingBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, max_length=200)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Anahtar Kelime')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blog', verbose_name='Blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogcategory', verbose_name='Kategori'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yazar'),
        ),
    ]