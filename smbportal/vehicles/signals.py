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
from django.shortcuts import reverse
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def notify_bike_created(sender, **kwargs):
    if kwargs.get("created"):
        bike = kwargs.get("instance")
        current_site = Site.objects.get_current()
        context = {
            "nickname": bike.nickname,
            "site_name": current_site.name,
            "bike_url": "https://{}{}".format(
                current_site.domain, bike.get_absolute_url())
        }
        send_mail(
            subject=render_to_string(
                "vehicles/mail/bike_created_subject.txt", context=context),
            message=render_to_string(
                "vehicles/mail/bike_created_message.txt", context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[bike.owner.email]
        )


def notify_bike_deleted(sender, **kwargs):
    bike = kwargs.get("instance")
    current_site = Site.objects.get_current()
    context = {
        "nickname": bike.nickname,
        "site_name": current_site.name,
        "bike_list_url": "https://{}{}".format(
            current_site.domain,
            reverse("bikes:list")
        )
    }
    send_mail(
        subject=render_to_string(
            "vehicles/mail/bike_deleted_subject.txt", context=context),
        message=render_to_string(
            "vehicles/mail/bike_deleted_message.txt", context=context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[bike.owner.email]
    )
