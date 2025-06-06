# Generated by Django 2.2.5 on 2020-05-28 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('squads', '0019_auto_20200527_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdata',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bill_data', to='accounts.CRMCard'),
        ),
        migrations.AlterField(
            model_name='billdata',
            name='squad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bill_data', to='squads.Squad'),
        ),
    ]
