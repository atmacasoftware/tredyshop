# Generated by Django 4.2.2 on 2023-08-20 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicesreceived',
            name='month',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], default='1', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invoicesreceived',
            name='year',
            field=models.CharField(choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], default='2023', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='issuedinvoices',
            name='edited_date',
            field=models.DateField(null=True, verbose_name='Fatura Düzenlenme Tarihi'),
        ),
        migrations.AddField(
            model_name='issuedinvoices',
            name='month',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], default='1', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='issuedinvoices',
            name='year',
            field=models.CharField(choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], default='2023', max_length=10, null=True),
        ),
    ]