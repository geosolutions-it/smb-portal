# Generated by Django 2.0.5 on 2018-05-30 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_enduserprofile_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enduserprofile',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male')], default='female', max_length=20),
        ),
        migrations.AlterField(
            model_name='mobilityhabitssurvey',
            name='end_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mobility_habits_surveys', to='profiles.EndUserProfile'),
        ),
    ]
