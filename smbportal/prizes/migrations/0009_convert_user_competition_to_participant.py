from django.db import migrations


def convert_to_participant(apps, schema_editor):
    """Add ``participant`` info to preexisting ``Winner`` instances """
    Winner = apps.get_model("prizes", "Winner")
    CompetitionParticipant = apps.get_model("prizes", "CompetitionParticipant")
    for winner in Winner.objects.all():
        participant = CompetitionParticipant(
            user=winner.user,
            competition=winner.competition,
            registration_status="approved",
            registration_justification="Manually migrated"
        )
        participant.save()
        winner.participant = participant
        winner.save()


def revert_to_previous(apps, schema_editor):
    Winner = apps.get_model("prizes", "Winner")
    for winner in Winner.objects.all():
        winner.user = winner.participant.user
        winner.competition = winner.participant.competition
        winner.save()


class Migration(migrations.Migration):

    dependencies = [
        ('prizes', '0008_auto_20190620_1008'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_participant,
            reverse_code=revert_to_previous
        )
    ]
