# Generated by Django 4.2.2 on 2023-08-14 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendyolBrand',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Kategori Adı')),
            ],
            options={
                'verbose_name': '7) Trendyol Markalar',
                'verbose_name_plural': '7) Trendyol Markalar',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='trendyolfirstcategory',
            options={'ordering': ['id'], 'verbose_name': '1) Trendyol 1. Kategori', 'verbose_name_plural': '1) Trendyol 1. Kategori'},
        ),
        migrations.AlterModelOptions(
            name='trendyolfivecategory',
            options={'ordering': ['id'], 'verbose_name': '5) Trendyol 5. Kategori', 'verbose_name_plural': '5) Trendyol 5. Kategori'},
        ),
        migrations.AlterModelOptions(
            name='trendyolfourcategory',
            options={'ordering': ['id'], 'verbose_name': '4) Trendyol 4. Kategori', 'verbose_name_plural': '4) Trendyol 4. Kategori'},
        ),
        migrations.AlterModelOptions(
            name='trendyolsecondcategory',
            options={'ordering': ['id'], 'verbose_name': '2) Trendyol 2. Kategori', 'verbose_name_plural': '2) Trendyol 2. Kategori'},
        ),
        migrations.AlterModelOptions(
            name='trendyolsixcategory',
            options={'ordering': ['id'], 'verbose_name': '6) Trendyol 6. Kategori', 'verbose_name_plural': '6) Trendyol 6. Kategori'},
        ),
        migrations.AlterModelOptions(
            name='trendyolthirdcategory',
            options={'ordering': ['id'], 'verbose_name': '3) Trendyol 3. Kategori', 'verbose_name_plural': '3) Trendyol 3. Kategori'},
        ),
    ]