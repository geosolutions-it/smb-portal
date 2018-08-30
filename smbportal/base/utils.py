#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging
from smtplib import SMTPServerDisconnected
from smtplib import SMTPSenderRefused

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.template.loader import render_to_string

from vehicles import models

logger = logging.getLogger(__name__)


def get_current_bike(view_kwargs, pk_kwarg_name="pk",
                     slug_kwarg_name="slug",
                     slug_attr_name="short_uuid"):
    try:
        bike = models.Bike.objects.get(pk=view_kwargs.get(pk_kwarg_name))
    except models.Bike.DoesNotExist:
        try:
            bike = models.Bike.objects.get(
                **{slug_attr_name: view_kwargs.get(slug_kwarg_name)})
        except models.Bike.DoesNotExist:
            bike = None
    return bike


def get_group_name(group_path):
    for group_name, group_paths in settings.KEYCLOAK["group_mappings"].items():
        if group_path in group_paths:
            result = group_name
            break
    else:
        result = None
    return result


def send_email_to_admins(subject_template, message_template, context=None):
    """Send email to admins

    Admins are all users that have the ``is_superuser`` attribute set to True
    plus all email addresses declared in ``settings.ADMINS`` (if any)

    """

    logger.debug("context: {}".format(context))

    superusers = get_user_model().objects.filter(is_superuser=True)
    destination_addresses = set(superusers.values_list("email", flat=True))
    logger.debug("destination_addresses: {}".format(destination_addresses))
    unique_recipients = set(settings.ADMINS).union(destination_addresses)
    logger.debug("unique_recipients: {}".format(unique_recipients))
    ctx = dict(context) if context is not None else {}
    send_mail(
        subject=render_to_string(subject_template, context=ctx),
        message=render_to_string(message_template, context=ctx),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(unique_recipients)
    )


def send_mail(*args, **kwargs):
    """Wrapper around django's ``send_mail`` that catches more errors"""
    try:
        mail.send_mail(*args, **kwargs)
    except (SMTPSenderRefused, SMTPServerDisconnected) as exc:
        logger.warning(
            "Could not send notification email: {}".format(str(exc)))
