# Generated by Django 3.2.21 on 2023-11-20 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpage', '0033_updatehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Izinler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ana_slider', models.BooleanField(default=False, verbose_name='Ana Slayt Ekranı')),
                ('kategori_gorme', models.BooleanField(default=False, verbose_name='Kategoleri Görme')),
                ('kategori_duzenleme', models.BooleanField(default=False, verbose_name='Kategori Düzenleme')),
                ('urun_ekleme', models.BooleanField(default=False, verbose_name='Ürün Ekleme')),
                ('urun_duzeneleme', models.BooleanField(default=False, verbose_name='Ürün Düzenleme')),
                ('kampanyali_urunler', models.BooleanField(default=False, verbose_name='Kampanyalı Ürün İşlemleri')),
                ('urun_ozellik_islemleri', models.BooleanField(default=False, verbose_name='Ürün Özellik İşlemleri')),
                ('tredyshop_siparisleri', models.BooleanField(default=False, verbose_name='TredyShop Sipariş İşlemleri')),
                ('trendyol_siparisleri', models.BooleanField(default=False, verbose_name='Trendyol Sipariş İşlemleri')),
                ('xml_islemleri', models.BooleanField(default=False, verbose_name='XML Yönetimi İşlemleri')),
                ('kullanici_ekleme', models.BooleanField(default=False, verbose_name='Kullanıcı Ekleme İşlemi')),
                ('kullanici_silme', models.BooleanField(default=False, verbose_name='Kullanıcı Silme İşlemi')),
                ('kullanici_duzenleme', models.BooleanField(default=False, verbose_name='Kullanıcı Düzenleme İşlemi')),
                ('kullanici_yetkilendirme', models.BooleanField(default=False, verbose_name='Kullanıcı Yetkilendirme İşlemi')),
                ('anasayfa_islemleri', models.BooleanField(default=False, verbose_name='Anasayfa İşlemleri')),
                ('hakkimizda_islemleri', models.BooleanField(default=False, verbose_name='Hakkımızda Sayfası İşlemleri')),
                ('trendyol_hesap_bilgileri', models.BooleanField(default=False, verbose_name='Trendyol Hesap Bilgileri')),
                ('trendyol_urun_girisi', models.BooleanField(default=False, verbose_name='Trendyol Ürün Girişi')),
                ('trendyol_stok_fiyat_guncelleme', models.BooleanField(default=False, verbose_name='Trendyol Stok & Fiyat Güncelleme')),
                ('trendyol_bilgi_guncelleme', models.BooleanField(default=False, verbose_name='Trendyol Bilgi Güncelleme')),
                ('trendyol_urun_silme', models.BooleanField(default=False, verbose_name='Trendyol Ürün Silme')),
                ('trendyol_urunleri', models.BooleanField(default=False, verbose_name='Trendyol Ürünlerine Erişim')),
                ('trendyol_siparis_ekle', models.BooleanField(default=False, verbose_name='Trendyol Sipariş Ekleme')),
                ('trendyol_istek_cevaplari', models.BooleanField(default=False, verbose_name='Trendyol İstek Cevapları')),
                ('kesilen_fatura', models.BooleanField(default=False, verbose_name='Kesilen Fatura İşlemleri')),
                ('alinan_fatura', models.BooleanField(default=False, verbose_name='Alınan Fatura İşlemleri')),
                ('harcamalar', models.BooleanField(default=False, verbose_name='Harcama İşlemleri')),
                ('gecmis_kayitlar', models.BooleanField(default=False, verbose_name='Geçmiş Kayıt İşlemleri')),
                ('istatistikler', models.BooleanField(default=False, verbose_name='İstatistiki Bilgilere Erişim')),
                ('aksyionlar', models.BooleanField(default=False, verbose_name='Aksiyonlara Erişim')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'İzinler',
                'verbose_name_plural': 'İzinler',
            },
        ),
    ]