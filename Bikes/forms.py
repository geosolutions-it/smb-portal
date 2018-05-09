from django.forms import ModelForm
from .models import Users


class UserForm(ModelForm):
    class Meta:
        model =Users
        exclude = []