# Generated by Django 3.2.21 on 2024-02-19 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0096_frontentheadercategory_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frontentheadercategory',
            old_name='status',
            new_name='is_publish',
        ),
    ]