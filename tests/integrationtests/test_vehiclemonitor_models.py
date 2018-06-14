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

pytestmark = pytest.mark.integration


@pytest.mark.xfail
def test_bike_observation_requires_position_if_not_address():
    raise NotImplementedError


@pytest.mark.xfail
def test_bike_observation_requires_address_if_not_position():
    raise NotImplementedError
