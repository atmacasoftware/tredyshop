# Generated by Django 3.2.21 on 2024-02-13 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ciceksepeti', '0007_ciceksepetikategori_parentcategoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciceksepetikategori',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ciceksepeti.ciceksepetikategori', verbose_name='Kategori Adı'),
        ),
    ]