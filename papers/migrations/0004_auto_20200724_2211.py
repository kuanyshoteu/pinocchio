# Generated by Django 2.2.5 on 2020-07-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20200724_2100'),
        ('papers', '0003_auto_20200724_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='estimater_ids',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='grades',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='is_homework',
        ),
        migrations.AddField(
            model_name='lesson',
            name='try_by',
            field=models.ManyToManyField(related_name='try_lessons', to='accounts.Profile'),
        ),
    ]
