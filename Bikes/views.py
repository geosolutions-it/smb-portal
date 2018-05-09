from django.shortcuts import render
from .forms import UserForm
# Create your views here.

#class based view and a mixin

#class Registration():
def home(request):
    
    Register = UserForm()
    
    return render(request,'Bikes/home.html',{"form":Register})
