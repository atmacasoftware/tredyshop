# Generated by Django 3.2.21 on 2023-12-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendyol', '0016_auto_20231205_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='trendyolmoreproductorder',
            name='status',
            field=models.CharField(choices=[('Yeni', 'Yeni'), ('Onaylandı', 'Onaylandı'), ('Hazırlanıyor', 'Hazırlanıyor'), ('Kargolandı', 'Kargolandı'), ('Tamamlandı', 'Tamamlandı'), ('İptal Edildi', 'İptal Edildi'), ('İade Edildi', 'İade Edildi'), ('Ödeme Yapılmadı', 'Ödeme Yapılmadı')], max_length=255, null=True, verbose_name='Durum'),
        ),
    ]