# Generated by Django 2.0 on 2019-07-24 10:42

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prizes', '0012_auto_20190620_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionOfInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='geometry')),
            ],
        ),
        migrations.CreateModel(
            name='PendingCompetitionParticipant',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('prizes.competitionparticipant',),
        ),
    ]
