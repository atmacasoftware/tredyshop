# Generated by Django 4.2.2 on 2023-08-14 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorymodel', '0007_trendyolfirstcategory_alter_subcategory_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendyolSecondCategory',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Kategori Adı')),
                ('parentId', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '4) Trendyol 2. Kategori',
                'verbose_name_plural': '4) Trendyol 2. Kategori',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='trendyolfirstcategory',
            options={'ordering': ['id'], 'verbose_name': '4) Trendyol 1. Kategori', 'verbose_name_plural': '4) Trendyol 1. Kategori'},
        ),
    ]