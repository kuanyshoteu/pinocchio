# Generated by Django 2.2.5 on 2019-12-08 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0007_financeclosed'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeclosed',
            name='bill',
            field=models.IntegerField(default=0),
        ),
    ]
