# Generated by Django 2.2.5 on 2019-11-07 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('todolist', '0001_initial'),
        ('accounts', '0001_initial'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('author_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='docfolders', to='accounts.Profile')),
                ('children', models.ManyToManyField(related_name='_documentfolder_children_+', to='documents.DocumentFolder')),
                ('files', models.ManyToManyField(related_name='docfolder', to='todolist.Document')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='docchilds', to='documents.DocumentFolder')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_docfolders', to='schools.School')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DocumentCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_type', models.TextField(default='')),
                ('object_id', models.IntegerField(null=True)),
                ('action', models.TextField(default='')),
                ('previous_parent', models.IntegerField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('full', models.BooleanField(default=False)),
                ('author_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doccache', to='accounts.Profile')),
            ],
        ),
    ]
