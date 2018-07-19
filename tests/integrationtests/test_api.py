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


@pytest.mark.parametrize("endpoint", [
    "api:my-bikes-list",
    "api:my-bike-observations-list",
    "api:my-bike-statuses-list",
    "api:my-tags-list",
])
@pytest.mark.django_db
def test_end_user_can_access_list_endpoint(endpoint, api_client, end_user):
    api_client.force_authenticate(user=end_user)
    response = api_client.get(reverse(endpoint))
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", [
    "api:bikes-list",
    "api:bike-observations-list",
    "api:bike-statuses-list",
    "api:tags-list",
    "api:users-list",
    "api:picture-galleries-list",
    "api:pictures-list",
])
@pytest.mark.django_db
def test_end_user_cannot_access_list_endpoint(endpoint, api_client, end_user):
    api_client.force_authenticate(user=end_user)
    response = api_client.get(reverse(endpoint))
    assert response.status_code == 403


@pytest.mark.parametrize("endpoint", [
    "api:bikes-list",
    "api:bike-observations-list",
    "api:bike-statuses-list",
    "api:tags-list",
    "api:users-list",
    "api:picture-galleries-list",
    "api:pictures-list",
])
def test_privileged_user_can_access_list_endpoint(endpoint, privileged_user,
                                                  api_client):
    api_client.force_authenticate(user=privileged_user)
    response = api_client.get(reverse(endpoint))
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", [
    "api:my-bikes-list",
    "api:my-bike-observations-list",
    "api:my-bike-statuses-list",
    "api:my-tags-list",
])
def test_privileged_user_cannot_access_list_endpoint(endpoint, privileged_user,
                                                     api_client):
    api_client.force_authenticate(user=privileged_user)
    response = api_client.get(reverse(endpoint))
    assert response.status_code == 403


@pytest.mark.django_db
def test_end_user_can_report_lost_bike(api_client, bike_owned_by_end_user):
    bike_url = reverse(
        "api:bikes-detail",
        kwargs={
            "short_uuid": bike_owned_by_end_user.short_uuid
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
            kwargs={"short_uuid": bike_owned_by_end_user.short_uuid}
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
            "bike": bike_owned_by_end_user.short_uuid,
            "epc": "some-fake-code"
        },
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_privileged_can_filter_bikes_using_tag_epc(api_client,
                                                   privileged_user,
                                                   bike_owned_by_end_user):
    api_client.force_authenticate(user=privileged_user)
    tag_epc = "123-321"
    PhysicalTag.objects.create(
        epc=tag_epc,
        bike=bike_owned_by_end_user
    )
    response = api_client.get(
        reverse("api:bikes-list"),
        kwargs={
            "tag": tag_epc
        }
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_privileged_user_can_add_new_bike_observation(api_client,
                                                      privileged_user,
                                                      bike_owned_by_end_user):
    bike_url = reverse(
        "api:bikes-detail",
        kwargs={
            "short_uuid": bike_owned_by_end_user.short_uuid
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
                "reporter_id": "fake_id",
                "reporter_type": "fake_type",
            }
        },
        format="json"
    )
    print(response.json())
    assert response.status_code == 201
