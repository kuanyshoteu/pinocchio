# Generated by Django 2.2.5 on 2020-05-30 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentfolder',
            old_name='files',
            new_name='docfiles',
        ),
    ]
