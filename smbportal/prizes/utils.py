#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Utility functions for dealing with prizes and competitions"""

import logging

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from base.utils import (
    notify_user,
    send_mail_to_recipients
)
from profiles.models import SmbUser

from . import models

logger = logging.getLogger(__name__)


def get_available_competitions(user: SmbUser):
    """Get competitions that a user is able to sign up to

    User is allowed to ask for registration if a competition:
    *  is not finished yet
    *  allows the user's age range

    """

    return models.CurrentCompetition.objects.exclude(
        competitionparticipant__user=user
    ).filter(
        age_groups__contains=[user.profile.age]
    )

def sign_up_for_competition(
        user: SmbUser,
        competition: models.Competition,
        request,
        approved: bool = False,
) -> models.CompetitionParticipant:
    """Sign a user up for a competition"""

    status = (
        models.CompetitionParticipant.APPROVED if approved else
        models.CompetitionParticipant.PENDING_MODERATION
    )
    participant, created = models.CompetitionParticipant.objects.get_or_create(
        competition=competition,
        user=user,
        defaults={
            "registration_status": status
        }
    )
    if created and approved:
        logger.info(
            f"User {user} has been signed up to competition {competition}")
    elif created and not approved:
        logger.info(
            f"User {user}'s request to enter competition {competition} is "
            f"pending moderation by an admin"
        )
        notify_competition_moderators(participant, request)
    else:
        logger.info(
            f"User {user} is already registered for competition {competition}")
    return participant


def notify_competition_moderators(
        participant: models.CompetitionParticipant,
        request
):
    """Notify moderators of the existence of a new participant"""
    subject_template = "prizes/mail/pending_moderation_request_subject.txt"
    message_template = "prizes/mail/pending_moderation_request_message.txt"
    qs = get_user_model().objects.filter(groups__name="competition_moderators")
    recipients = set([mod.email or mod.username for mod in qs])
    send_mail_to_recipients(
        recipients=recipients,
        subject_template=subject_template,
        message_template=message_template,
        context={
            "participant": participant,
            "site_name": get_current_site(request),
        }
    )


def moderate_competition_participation_request(
        participants: QuerySet,
        status: str,
        request
):
    num_moderated = 0
    for participant in participants:
        participant.registration_status = status
        participant.save()
        num_moderated += 1
        notify_competition_participant(participant, request)
    return num_moderated


def notify_competition_participant(
        participant: models.CompetitionParticipant,
        request
):
    status = participant.registration_status
    message = {
        "message_name": "competition_participation_moderated",
        "competition_id": participant.competition.id,
        "registration_status": status

    }
    notify_user(participant.user, message)
    email_address = participant.user.email
    if email_address:
        send_mail_to_recipients(
            recipients=[email_address],
            subject_template="prizes/mail/request_moderated_subject.txt",
            message_template="prizes/mail/request_moderated_message.txt",
            context={
                "site_name": get_current_site(request),
                "participant": participant,
                "approved": (
                    True if status == models.CompetitionParticipant.APPROVED
                    else False
                )
            }
        )
