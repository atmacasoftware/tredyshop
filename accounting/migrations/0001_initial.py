# Generated by Django 3.2.21 on 2024-03-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpensesIncurred',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True, verbose_name='Ödeme Adı')),
                ('company', models.CharField(max_length=500, null=True, verbose_name='Ödeme Yapılan Yer')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='Ödeme Tutarı')),
                ('status', models.CharField(blank=True, choices=[('Ödenecek', 'Ödenecek'), ('Ödendi', 'Ödendi')], max_length=20, null=True, verbose_name='Ödeme Durumu')),
                ('image', models.ImageField(blank=True, null=True, upload_to='img/accounting/', verbose_name='Fatura')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
            ],
            options={
                'verbose_name': '1) Yapılan Ödemeler',
                'verbose_name_plural': '1) Yapılan Ödemeler',
                'ordering': ['created_at'],
            },
        ),
    ]
