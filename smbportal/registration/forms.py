from django.forms import ModelForm
from smbportal.profiles.models import EndUserProfile
from django.forms.widgets import Textarea, TextInput,EmailInput





class EndUserForm(ModelForm):
    
    class Meta:
        model = EndUserProfile
        exclude = []
        
        widgets = {
            'email':EmailInput(attrs={'size': 20}),
            'username':TextInput(attrs={'size':20}),
            
            
            }