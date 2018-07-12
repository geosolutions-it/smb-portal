from django import forms
from django.utils.translation import gettext as _

from . import models


class SmbUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        include_accept_terms_field = kwargs.pop(
            "include_accept_terms_field", None)
        super().__init__(*args, **kwargs)
        if include_accept_terms_field is not None:
            del self.fields["accepted_terms_of_service"]

    class Meta:
        model = models.SmbUser
        fields = (
            "nickname",
            "language_preference",
            "accepted_terms_of_service",
        )

    def clean_accepted_terms_of_service(self):
        data = self.cleaned_data.get("accepted_terms_of_service")
        if not data:
            raise forms.ValidationError(
                _("Did not accept the portal's Terms of Service"))
        return data


class EndUserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.EndUserProfile
        fields = (
            "bio",
            "gender",
            "age",
            "occupation",
            "phone_number",
        )
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    }
                ),
            "gender": forms.RadioSelect(),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "js-states form-control",
                    "pattern": r"^\+\d{8,15}$",
                    "placeholder": "+99999999",
                    "title": "+00000000",
                }
            ),
        }


class PrivilegedUserProfileForm(forms.ModelForm):

    class Meta:
        model = models.PrivilegedUserProfile
        fields = ()


class UserMobilityHabitsForm(forms.ModelForm):

    class Meta:
        model = models.MobilityHabitsSurvey
        fields = (
            "end_user",
            "public_transport_usage",
            "uses_bike_sharing_services",
            "uses_electrical_car_sharing_services",
            "uses_fuel_car_sharing_services",
            "bicycle_usage",
        )
        widgets = {
            "end_user": forms.HiddenInput(),
            "public_transport_usage": forms.Select(
                attrs={
                    "class": "js-states form-control select_2",
                    "id": "select2",
                }
            ),
            "uses_bike_sharing_services": forms.NullBooleanSelect(
                attrs={
                    "class": "js-states form-control select_2",
                    "id": "select2",
                }
            ),
            "uses_electrical_car_sharing_services": forms.NullBooleanSelect(
                attrs={
                    "class": "js-states form-control select_2",
                    "id": "select2",
                }
            ),
            "uses_fuel_car_sharing_services": forms.NullBooleanSelect(
                attrs={
                    "class": "js-states form-control select_2",
                    "id": "select2",
                }
            ),
            "bicycle_usage": forms.Select(
                attrs={
                    "class": "js-states form-control select_2",
                    "id": "select2",
                }
            )
        }
