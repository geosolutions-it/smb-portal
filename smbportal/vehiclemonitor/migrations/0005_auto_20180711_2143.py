# Generated by Django 2.0.5 on 2018-07-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclemonitor', '0004_remove_bikeobservation_reporter'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikeobservation',
            name='reporter_id',
            field=models.CharField(default='placeholder_id', max_length=50, verbose_name='reporter id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bikeobservation',
            name='reporter_name',
            field=models.CharField(default='placeholder_name', max_length=50, verbose_name='reporter name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bikeobservation',
            name='reporter_type',
            field=models.CharField(default='placeholder_type', max_length=50, verbose_name='reporter type'),
            preserve_default=False,
        ),
    ]
