# Generated by Django 2.0 on 2018-10-18 11:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prizes', '0003_competitionprize_prize_attribution_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='closing_leaderboard',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='leaderboard calculated at the time the competition was closed. Winners are assigned from the score in this leaderboard', null=True, verbose_name='closing leaderboard'),
        ),
        migrations.AlterField(
            model_name='competitionprize',
            name='prize_attribution_template',
            field=models.TextField(blank=True, help_text="Message shown to the user when the prize is won. This string is treated as a normal django template and rendered with a context that has the following variables: `score`, `rank`. The `django.contrib.humanize` is available. Example: The string 'Congratulations, you got {{ rank|ordinal }} place with a score of {{ score }}' would get rendered as 'Congratulations, you got 1st place with a score of 2061'", verbose_name='prize attribution template'),
        ),
    ]
