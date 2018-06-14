#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from urllib.parse import urlparse

from django.urls import reverse
import pytest

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_create_profile_requires_login(client, settings):
    response = client.get(reverse("profile:create"))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302
