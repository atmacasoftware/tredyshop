# Generated by Django 3.2.21 on 2023-12-15 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0054_auto_20231215_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazonfiyatayarla',
            name='kar_marji',
        ),
        migrations.RemoveField(
            model_name='hepsiburadafiyatayarla',
            name='kar_marji',
        ),
        migrations.RemoveField(
            model_name='pttavmfiyatayarla',
            name='kar_marji',
        ),
        migrations.RemoveField(
            model_name='trendyolfiyatayarla',
            name='kar_marji',
        ),
        migrations.CreateModel(
            name='KarMarji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslangic', models.FloatField(null=True, verbose_name='Başlangıç Fiyatı')),
                ('bitis', models.FloatField(null=True, verbose_name='Bitiş Fiyatı')),
                ('kar_maji', models.FloatField(null=True, verbose_name='Kar Marjı')),
                ('amazon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.amazonfiyatayarla')),
                ('hepsiburada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.hepsiburadafiyatayarla')),
                ('pttavm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.pttavmfiyatayarla')),
                ('tredyshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.tredyshopfiyatayarla')),
                ('trendyol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.trendyolfiyatayarla')),
            ],
        ),
    ]