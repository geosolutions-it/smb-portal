#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from unittest import mock

import pytest

from base import utils

pytestmark = pytest.mark.unit


@mock.patch("base.utils.mail", autospec=True)
@mock.patch("base.utils.render_to_string", autospec=True)
def test_send_email_to_admins(mock_render_to_string, mock_django_mail,
                              settings, django_user_model):
    subject_template = "fake_subject_template"
    rendered_subject = "subject"
    message_template = "fake_message_template"
    rendered_message = "message"
    context = {}
    sender_address = "sender@mail.com"
    recipient_address = "receiver@mail.com"
    settings.ADMINS = []
    settings.DEFAULT_FROM_EMAIL = sender_address

    mocked_qs = mock.MagicMock(spec=django_user_model.objects)
    mocked_qs.filter.return_value = mocked_qs
    mocked_qs.values_list.return_value = [recipient_address]
    mock_render_to_string.side_effect = [rendered_subject, rendered_message]

    with mock.patch.object(django_user_model, "objects", new=mocked_qs):
        utils.send_email_to_admins(
            subject_template,
            message_template,
            context
        )
    mock_render_to_string.assert_has_calls([
        mock.call(subject_template, context),
        mock.call(message_template, context)
    ])
    mock_django_mail.send_mail.assert_called_with(
        subject=rendered_subject,
        message=rendered_message,
        from_email=sender_address,
        recipient_list=[recipient_address]
    )
