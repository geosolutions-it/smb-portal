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


@pytest.mark.parametrize("accepted_terms, expected", [
    (None, False),
    (False, False),
    (True, True),
])
@pytest.mark.django_db
def test_smbuserform_requires_accepting_terms(end_user, accepted_terms,
                                              expected):
    form = forms.SmbUserForm(
        instance=end_user,
        data={
            "language_preference": "en",
            "accepted_terms_of_service": accepted_terms,
        }
    )
    valid = form.is_valid()
    assert valid == expected


@pytest.mark.parametrize("language, expected", [
    (None, False),
    ("en", True),
    ("it", True),
])
@pytest.mark.django_db
def test_smbuserform_requires_choosing_language(end_user, language,
                                                expected):
    form = forms.SmbUserForm(
        instance=end_user,
        data={
            "accepted_terms_of_service": True,
            "language_preference": language,
        }
    )
    valid = form.is_valid()
    assert valid == expected
