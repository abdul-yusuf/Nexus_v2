# Generated by Django 3.2 on 2022-12-22 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20221222_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='received',
            new_name='delivered',
        ),
    ]