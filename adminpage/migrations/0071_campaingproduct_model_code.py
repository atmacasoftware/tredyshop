# Generated by Django 3.2.21 on 2023-12-21 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0070_alter_issuedinvoices_tax_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaingproduct',
            name='model_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Model Kodu'),
        ),
    ]