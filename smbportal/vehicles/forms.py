from django import forms
from . import Bike
class SmbUserForm(forms.ModelForm):
    class Meta:
        model = Bike
        exclude = []