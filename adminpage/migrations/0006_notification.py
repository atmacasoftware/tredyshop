# Generated by Django 4.2.2 on 2023-08-25 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpage', '0005_trendyol_iadeadresid_1_trendyol_iadeadresid_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noti_type', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], max_length=20, verbose_name='Bildirim Tipi')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Bildirim Başlığı')),
                ('detail', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Bildirim İçeriği')),
                ('is_read', models.BooleanField(default=False, verbose_name='Okundu mu?')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_customer', to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_user', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': '4) Bildirimler',
                'verbose_name_plural': '4) Bildirimler',
                'ordering': ['created_at'],
            },
        ),
    ]