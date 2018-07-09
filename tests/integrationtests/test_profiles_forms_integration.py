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

from profiles import models
from profiles import forms

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("params", [
    {
        "age": models.EndUserProfile.AGE_OLDER_THAN_SIXTY_FIVE,
        "gender": models.EndUserProfile.FEMALE_GENDER,
    }
])
@pytest.mark.django_db
def test_enduserprofileform_update(end_user_with_profile, params):
    profile = end_user_with_profile.profile
    form = forms.EndUserProfileForm(
        instance=profile,
        data={k: str(v) for k, v in params.items()}
    )
    valid = form.is_valid()
    print(form.errors)
    assert valid
    form.save()
    profile.refresh_from_db()
    for k, v in params.items():
        assert getattr(profile, k) == v
