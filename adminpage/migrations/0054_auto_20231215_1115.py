# Generated by Django 3.2.21 on 2023-12-15 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0053_auto_20231215_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='hepsiburadafiyatayarla',
            name='process',
            field=models.FloatField(null=True, verbose_name='İşlem Bedeli (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='amazonfiyatayarla',
            name='commission',
            field=models.FloatField(null=True, verbose_name='Amazon Komisyonu'),
        ),
        migrations.AlterField(
            model_name='amazonfiyatayarla',
            name='kargo',
            field=models.FloatField(null=True, verbose_name='Kargo Maliyeti (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='amazonfiyatayarla',
            name='service',
            field=models.FloatField(null=True, verbose_name='Hizmet Bedeli (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='hepsiburadafiyatayarla',
            name='kargo',
            field=models.FloatField(null=True, verbose_name='Kargo Maliyeti (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='hepsiburadafiyatayarla',
            name='service',
            field=models.FloatField(null=True, verbose_name='Hizmet Bedeli (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='pttavmfiyatayarla',
            name='commission',
            field=models.FloatField(null=True, verbose_name='PTT Avm Komisyonu'),
        ),
        migrations.AlterField(
            model_name='pttavmfiyatayarla',
            name='kargo',
            field=models.FloatField(null=True, verbose_name='Kargo Maliyeti (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='pttavmfiyatayarla',
            name='service',
            field=models.FloatField(null=True, verbose_name='Hizmet Bedeli (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='tredyshopfiyatayarla',
            name='kargo',
            field=models.FloatField(null=True, verbose_name='Kargo Maliyeti (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='trendyolfiyatayarla',
            name='kargo',
            field=models.FloatField(null=True, verbose_name='Kargo Maliyeti (KDV Dahil)'),
        ),
        migrations.AlterField(
            model_name='trendyolfiyatayarla',
            name='service',
            field=models.FloatField(null=True, verbose_name='Hizmet Bedeli (KDV Dahil)'),
        ),
    ]