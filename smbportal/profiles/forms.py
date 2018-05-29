from django import forms
from . import models

class EndUserDetailViewForm(forms.ModelForm):
    class Meta:
        model = models.EndUserProfile
        exclude = [
            'date_updated',
            ]
        widgets = {
            'user': forms.HiddenInput(),
            'bio': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-rounded',
                    'size':'10',
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'size':'20','id':"select2",
                    }
                ),
            #'user_avatar': forms.ImageField(),
        }

class EndUserCreateViewForm(forms.ModelForm):
    class Meta:
        model = models.EndUserProfile
        exclude = [
            'date_updated',
            ]
        widgets = {
            'user': forms.HiddenInput(),
            'bio': forms.TextInput(
                attrs={
                    'class': 'form-control form-control',
                    
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                ),
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            #'user_avatar': forms.ImageField(),
        }
        
        
class UserMobilityHabitsForm(forms.ModelForm):
    class Meta: 
        model = models.MobilityHabitsSurvey
        exclude = [
            'date_answered',
            
            ]
        widgets = {
            'end_user': forms.HiddenInput(),
            'public_transport_usage': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                ),
            'uses_bike_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                ),
            'uses_electrical_car_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                ),
            'uses_fuel_car_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                ),
            'bicycle_usage':forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id':"select2",
                    }
                )
        }
        