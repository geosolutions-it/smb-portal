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

from django.contrib.auth.models import Group
from django.urls import reverse
import pytest

import profiles.models
import vehicles.models
import vehicles.views

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_bike_list_requires_login(client, settings):
    response = client.get(reverse("bikes:list"))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_list_denied_if_not_member_endusers_group(rf, django_user_model):
    user = django_user_model.objects.create(username="user")

    request = rf.get(reverse("bikes:list"))
    request.user = user
    response = vehicles.views.BikeListView.as_view()(request)
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == reverse("profile:create")
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_list_accepted_if_member_endusers_group(rf, end_user):
    request = rf.get(reverse("bikes:list"))
    request.user = end_user
    response = vehicles.views.BikeListView.as_view()(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_bike_list_only_returns_owned_bikes(rf, django_user_model, settings):
    user1 = django_user_model.objects.create(username="user1")
    profiles.models.EndUserProfile.objects.create(user=user1)
    user2 = django_user_model.objects.create(username="user2")
    end_users_group = Group.objects.create(name=settings.END_USER_PROFILE)
    end_users_group.user_set.add(user1, user2)
    bike1 = vehicles.models.Bike.objects.create(nickname="bike1", owner=user1)
    vehicles.models.Bike.objects.create(nickname="bike2", owner=user2)
    request = rf.get(reverse("bikes:list"))
    request.user = user1
    response = vehicles.views.BikeListView.as_view()(request)
    assert list(response.context_data["bikes"]) == [bike1]


@pytest.mark.django_db
def test_bike_create_requires_login(client, settings):
    response = client.get(reverse("bikes:create"))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_detail_requires_login(client, settings, admin_user):
    bike = vehicles.models.Bike.objects.create(
        nickname="test",
        owner=admin_user
    )
    response = client.get(
        reverse("bikes:detail", kwargs={"slug": bike.short_uuid}))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_update_requires_login(client, settings, admin_user):
    bike = vehicles.models.Bike.objects.create(
        nickname="test",
        owner=admin_user
    )
    response = client.get(
        reverse("bikes:update", kwargs={"slug": bike.short_uuid}))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_delete_requires_login(client, settings, admin_user):
    bike = vehicles.models.Bike.objects.create(
        nickname="test",
        owner=admin_user
    )
    response = client.get(
        reverse("bikes:delete", kwargs={"slug": bike.short_uuid}))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_bike_picture_upload_requires_login(client, settings, admin_user):
    bike = vehicles.models.Bike.objects.create(
        nickname="test",
        owner=admin_user
    )
    response = client.get(
        reverse("bikes:picture-upload", kwargs={"slug": bike.short_uuid}))
    redirected_to = urlparse(response["Location"])
    assert redirected_to.path == settings.LOGIN_URL
    assert response.status_code == 302
