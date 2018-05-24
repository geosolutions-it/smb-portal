from django.forms import ModelForm
from smbportal.profiles.models import EndUserProfile
from django.forms.widgets import Textarea, TextInput,EmailInput, NumberInput,\
    PasswordInput





class EndUserForm(ModelForm):
    
    class Meta:
        model = EndUserProfile
        exclude = []
        
        widgets = {
            'email':EmailInput(attrs={'size': 20,'class':'form-control'}),
            'username':TextInput(attrs={'size':20,'class':'form-control'}),
            'first_name':TextInput(attrs={'class':'form-control'}),
            'last_name':TextInput(attrs={'class':'form-control'}),
            'phone_number':NumberInput(attrs={'class':'form-control'}),
            'password':PasswordInput(attrs={'class':'form-control'}),
            
            
            }