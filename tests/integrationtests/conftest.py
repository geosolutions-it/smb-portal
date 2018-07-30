from bossoidc.models import Keycloak
from django.contrib.auth.models import Group
import pytest
from rest_framework.test import APIClient

import profiles.models
from vehicles.models import Bike


@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.logout()
    client.credentials()


@pytest.fixture
def privileged_user(db, django_user_model, settings):
    group = Group.objects.get_or_create(
        name=settings.PRIVILEGED_USER_PROFILE)[0]
    user = django_user_model.objects.create(username="privileged")
    Keycloak.objects.create(user=user, UID="keycloakuuid-abcd-456")
    group.user_set.add(user)
    group.save()
    return user


@pytest.fixture
def end_user(db, django_user_model, settings):
    group = Group.objects.get_or_create(
        name=settings.END_USER_PROFILE)[0]
    user = django_user_model.objects.create(username="enduser")
    Keycloak.objects.create(user=user, UID="keycloakuuid-abcd-123")
    group.user_set.add(user)
    group.save()
    return user


@pytest.fixture
def end_user_with_profile(db, end_user):
    profiles.models.EndUserProfile.objects.create(
        user=end_user,
        gender=profiles.models.EndUserProfile.FEMALE_GENDER,
        age=profiles.models.EndUserProfile.AGE_YOUNGER_THAN_NINETEEN,
    )
    return end_user


@pytest.fixture
def bike_owned_by_end_user(db, end_user):
    bike = Bike.objects.create(
        nickname="tester_bike",
        owner=end_user
    )
    return bike
