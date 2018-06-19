#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import pytest
from rest_framework.reverse import reverse

from vehicles.models import PhysicalTag

pytestmark = pytest.mark.integration

# TODO: also test that other user types cannot perform these actions


@pytest.mark.django_db
def test_end_user_can_report_lost_bike(api_client, bike_owned_by_end_user):
    bike_url = reverse(
        "api:bikes-detail",
        kwargs={
            "pk": bike_owned_by_end_user.pk
        }
    )
    api_client.force_authenticate(user=bike_owned_by_end_user.owner)
    response = api_client.post(
        reverse("api:my-bike-statuses-list"),
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [1, -1]},
            "properties": {
                "bike": bike_url,
                "lost": True,
                "details": ""
            }
        },
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_privileged_user_can_access_bike_details(api_client, privileged_user,
                                                 bike_owned_by_end_user):
    api_client.force_authenticate(user=privileged_user)
    response = api_client.get(
        reverse(
            "api:bikes-detail",
            kwargs={"pk": bike_owned_by_end_user.pk}
        )
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_privileged_user_can_register_new_tag(api_client, privileged_user,
                                              bike_owned_by_end_user):
    api_client.force_authenticate(user=privileged_user)
    response = api_client.post(
        reverse("api:tags-list"),
        {
            "bike": reverse(
                "api:bikes-detail",
                kwargs={
                    "pk": bike_owned_by_end_user.pk
                }
            ),
            "epc": "some-fake-code"
        },
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.xfail(reason="Did not implement API filtering yet")
def test_privileged_can_filter_bikes_using_tag_epc(api_client,
                                                   privileged_user,
                                                   bike_owned_by_end_user):
    api_client.force_authenticate(user=privileged_user)
    tag_epc = "123-321"
    PhysicalTag.objects.create(
        epc=tag_epc,
        bike=bike_owned_by_end_user
    )
    response = api_client.post(
        reverse(
            "api:tags-list",
            kwargs={
                "epc": tag_epc
            }
        ),
        format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_privileged_user_can_add_new_bike_observation(api_client,
                                                      privileged_user,
                                                      bike_owned_by_end_user):
    bike_url = reverse(
        "api:bikes-detail",
        kwargs={
            "pk": bike_owned_by_end_user.pk
        }
    )
    reporter_url = reverse(
        "api:users-detail",
        kwargs={
            "pk": str(bike_owned_by_end_user.owner.keycloak.UID)
        }
    )
    api_client.force_authenticate(user=privileged_user)
    response = api_client.post(
        reverse("api:bike-observations-list"),
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
            },
            "properties": {
                "bike": bike_url,
                "reporter": reporter_url,
            }
        },
        format="json"
    )
    assert response.status_code == 201
