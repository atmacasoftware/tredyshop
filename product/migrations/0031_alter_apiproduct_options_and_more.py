# Generated by Django 4.2.2 on 2023-09-12 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_apiproduct_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apiproduct',
            options={'verbose_name': '1) Ürünler', 'verbose_name_plural': '1) Ürünler'},
        ),
        migrations.AlterField(
            model_name='dislikeproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislike_product', to='product.apiproduct'),
        ),
        migrations.AlterField(
            model_name='likeproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_product', to='product.apiproduct'),
        ),
        migrations.AlterField(
            model_name='question',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.apiproduct', verbose_name='Ürün'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.apiproduct'),
        ),
        migrations.AlterField(
            model_name='reviewratingimages',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.apiproduct'),
        ),
        migrations.AlterField(
            model_name='stockalarm',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.apiproduct', verbose_name='Ürün'),
        ),
    ]