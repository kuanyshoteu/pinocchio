# Generated by Django 2.2.5 on 2020-03-08 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200303_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='', null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mails', to='accounts.CRMCard')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
