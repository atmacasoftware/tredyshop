# Generated by Django 3.2.21 on 2023-10-30 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0050_auto_20231027_0652'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Paça Tipi')),
            ],
        ),
        migrations.CreateModel(
            name='Pocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Cep')),
            ],
        ),
        migrations.CreateModel(
            name='Waist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Bel')),
            ],
        ),
        migrations.AddField(
            model_name='apiproduct',
            name='legtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.legtype', verbose_name='Paça Tipi'),
        ),
        migrations.AddField(
            model_name='apiproduct',
            name='pocket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.pocket', verbose_name='Cep'),
        ),
        migrations.AddField(
            model_name='apiproduct',
            name='waist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.waist', verbose_name='Bel'),
        ),
    ]