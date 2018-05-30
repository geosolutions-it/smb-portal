from django import forms
from . import models

class EndUserDetailViewForm(forms.ModelForm):
    
    
    class Meta:
        model = models.EndUserProfile
        fields = (
            'user',
            'gender',
            'phone_number',
            'bio',
            )
        widgets = {
            'user': forms.HiddenInput(),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': "select2",'rows':'3'
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'js-states form-control',
                    'id':'select2',
                    }
                ),
            
        } 

class EndUserCreateViewForm(forms.ModelForm):
    
    
    class Meta:
        model = models.EndUserProfile
        fields = (
            'user','bio',
            'gender',
            'phone_number',
           
            
            
            )
        
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
                    'id': "select2",
                    }
                ),
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'js-states form-control',
                    'id':'select2',
                    }
                ),
            
        }
        
        
class EndUserUpdateViewForm(forms.ModelForm):
    
    
    class Meta:
        model = models.EndUserProfile
        fields = (
            'user','bio',
            'gender',
            'phone_number',
            
            
            )
        
        widgets = {
            'user': forms.HiddenInput(),
            'bio': forms.TextInput(
                attrs={
                    'class': 'form-control form-control',
                    'id': "select2",
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'js-states form-control',
                    'id':'select2',
                    }
                ),
            
        }        
        
class UserMobilityHabitsForm(forms.ModelForm):
    
    
    class Meta: 
        model = models.MobilityHabitsSurvey
        fields = (
            'end_user', 'public_transport_usage',
            'uses_bike_sharing_services',
            'uses_electrical_car_sharing_services',
            'uses_fuel_car_sharing_services',
            'bicycle_usage',
            )
        
        widgets = {
            'end_user': forms.HiddenInput(),
            'public_transport_usage': forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'uses_bike_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'uses_electrical_car_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'uses_fuel_car_sharing_services': forms.NullBooleanSelect(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                ),
            'bicycle_usage':forms.Select(
                attrs={
                    'class': 'js-states form-control select_2',
                    'id': "select2",
                    }
                )
        }
     
class PrizeManagerProfileDetailViewForm(forms.ModelForm):
    
    class Meta:
        model = models.PrizeManagerProfile 
        fields = (
            'organization',
            'language_preference',
            'acceptance_of_policy',
            )  