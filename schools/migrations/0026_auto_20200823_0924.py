# Generated by Django 2.2.5 on 2020-08-23 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0025_auto_20200820_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribepay',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
