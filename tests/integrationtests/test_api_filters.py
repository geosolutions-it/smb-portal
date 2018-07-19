#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import uuid
import pytest

from api import filters
import vehicles.models
import vehiclemonitor.models

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("uuid_slice", [
    slice(None),  # equivalent to [:]
    slice(0, 3)  # equivalent to [0:3]
])
def test_bikefilterset_filter_with_id(bike_owned_by_end_user, uuid_slice):
    filter_uuid = bike_owned_by_end_user.short_uuid
    filter_set = filters.BikeFilterSet(
        data={
            "short_uuid": filter_uuid[uuid_slice]
        },
        queryset=vehicles.models.Bike.objects.all()
    )
    result = list(filter_set.qs)
    assert result[0] == bike_owned_by_end_user


@pytest.mark.parametrize("tag_slice", [
    slice(None),  # equivalent to [:]
    slice(0, 3)  # equivalent to [0:3]
])
def test_bikefilterset_filter_with_tag(bike_owned_by_end_user, tag_slice):
    tag = vehicles.models.PhysicalTag.objects.create(
        bike=bike_owned_by_end_user,
        epc=uuid.uuid4()
    )
    filter_set = filters.BikeFilterSet(
        data={
            "tag": str(tag.epc)[tag_slice]
        },
        queryset=vehicles.models.Bike.objects.all()
    )
    result = list(filter_set.qs)
    assert result[0] == bike_owned_by_end_user


def test_bikeobservationfilterset_with_id(bike_owned_by_end_user,
                                          privileged_user):
    addresses = ["place1", "place2"]
    for address in addresses:
        vehiclemonitor.models.BikeObservation.objects.create(
            bike=bike_owned_by_end_user,
            reporter_id=privileged_user.pk,
            address=address
        )
    filter_set = filters.BikeObservationFilterSet(
        data={
            "bike": str(bike_owned_by_end_user.short_uuid)
        },
        queryset=vehiclemonitor.models.BikeObservation.objects.all()
    )
    result = list(filter_set.qs)
    assert result == list(bike_owned_by_end_user.observations.all())
