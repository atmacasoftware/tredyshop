# Generated by Django 4.2.2 on 2023-07-22 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorymodel', '0002_alter_maincategory_options_alter_subcategory_options_and_more'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subbottomcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subbottom_category', to='categorymodel.subbottomcategory', verbose_name='3. Düzey Kategori'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_category', to='categorymodel.maincategory', verbose_name='1. Düzey Kategori'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='categorymodel.subcategory', verbose_name='2. Düzey Kategori'),
        ),
    ]