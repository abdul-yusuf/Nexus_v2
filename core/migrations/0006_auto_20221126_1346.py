# Generated by Django 3.1 on 2022-11-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20221126_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='option',
            field=models.CharField(blank=True, choices=[('O', 'Online'), ('D', 'On Delivery')], max_length=1, null=True),
        ),
    ]
