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

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import models

logger = logging.getLogger(__name__)


def notify_profile_created(sender, **kwargs):
    sender_classes = (
        models.EndUserProfile,
        models.PrivilegedUserProfile,
    )
    if sender in sender_classes and kwargs.get("created"):
        logger.debug("profile created")
        profile = kwargs.get("instance")
        user = profile.user
        current_site = Site.objects.get_current()
        profile_type = profile.__class__.__name__.lower().replace(
            "profile", "")
        context = {
            "site_name": current_site.name,
            "profile_type": profile_type,
            "username": user.username,
            "profile_url": "https://{}{}".format(
                current_site.domain, user.get_absolute_url())
        }
        send_mail(
            subject=render_to_string(
                "profiles/mail/profile_created_subject.txt", context=context),
            message=render_to_string(
                "profiles/mail/profile_created_message.txt", context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
