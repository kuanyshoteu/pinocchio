# Generated by Django 2.2.5 on 2020-08-12 23:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0022_auto_20200625_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='money_update_date',
        ),
        migrations.AddField(
            model_name='school',
            name='version_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
