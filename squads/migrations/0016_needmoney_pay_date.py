# Generated by Django 2.2.5 on 2020-05-26 02:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('squads', '0015_needmoney_pay_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='needmoney',
            name='pay_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
