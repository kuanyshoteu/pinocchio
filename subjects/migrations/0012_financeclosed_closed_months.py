# Generated by Django 2.2.5 on 2019-12-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0011_auto_20191213_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeclosed',
            name='closed_months',
            field=models.IntegerField(default=0),
        ),
    ]
