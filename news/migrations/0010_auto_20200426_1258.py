# Generated by Django 2.2.5 on 2020-04-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20200423_0803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='done_by',
        ),
        migrations.RemoveField(
            model_name='postpart',
            name='content',
        ),
        migrations.RemoveField(
            model_name='postpart',
            name='show',
        ),
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
