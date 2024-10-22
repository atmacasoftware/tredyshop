# Generated by Django 3.2.21 on 2024-03-03 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorymodel', '0001_initial'),
        ('product', '0005_auto_20240302_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='product.brand', verbose_name='Marka'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_category', to='categorymodel.maincategory', verbose_name='1. Düzey Kategori'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subbottomcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subbottom_category', to='categorymodel.subbottomcategory', verbose_name='3. Düzey Kategori'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='categorymodel.subcategory', verbose_name='2. Düzey Kategori'),
        ),
    ]
