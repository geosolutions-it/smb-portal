# Generated by Django 2.0 on 2018-08-10 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0014_auto_20180809_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='vehicle_id',
            field=models.CharField(blank=True, help_text='Identifier of the vehicle used, if any', max_length=255, null=True),
        ),
    ]
