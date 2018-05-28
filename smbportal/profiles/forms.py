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
            'bio': forms.TextInput(attrs={'class': 'form-control form-control-rounded','size':'10'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-rounded','size':'10'})
        }
        
        
class UserMobilityHabitsForm(forms.ModelForm):
    class Meta: 
        model = models.MobilityHabitsSurvey
        exclude = [
            'date_answered',
            
            ]
        widgets = {
            'end_user': forms.HiddenInput(),
            'public_transport_usage': forms.Select(attrs={'class': 'form-control form-control-rounded','size':'10'}),
            'uses_bike_sharing_services': forms.NullBooleanSelect(attrs={'class': 'form-control form-control-rounded','size':'10'}),
            'uses_electrical_car_sharing_services': forms.NullBooleanSelect(attrs={'class': 'form-control form-control-rounded','size':'10'}),
            'uses_fuel_car_sharing_services': forms.NullBooleanSelect(attrs={'class': 'form-control form-control-rounded','size':'10'}),
            'bicycle_usage':forms.Select(attrs={'class': 'form-control form-control-rounded','size':'10'})
        }
        