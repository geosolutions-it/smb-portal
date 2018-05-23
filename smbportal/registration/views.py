from django.shortcuts import render
from django.views.generic import \
ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from smbportal.registration.models import  User, Prize 
from smbportal.profiles.models import EndUserProfile
from smbportal.vehicles.models import Vehicle, Tag
from smbportal.profiles.models import EndUserProfile
from multiprocessing.sharedctypes import template
# Create your views here.
from rest_framework import serializers

# django-restfull framework
from smbportal.registration.serializers import \
VehicleSerializer, PrizeSerializer, UserSerializer, \
TagSerializer, ReceiptSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from django.views import generic
import profile


class BikeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    template_name = 'registration/ViewVehicles.html'
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()
        

class PrizeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = EndUserProfile.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
        
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
        
class newuser(CreateView):
    model = EndUserProfile
    fields = (
        'username', 'password','email','gender','profile_type',
         'first_name', 'last_name','phone_number',
        )
    exclude = []
    template_name = 'registration/newuser.html'
    success_url = "http://localhost:8000/registration/home/"
    
    
class vehicleList(ListView):
    model = Vehicle
    # queryset = bike.objects.all(owner_id=request.EndUserProfile)
    fields = (
        'bikes_id', 'owner_id', 
        'model', 'created_at'
        )
    template_name = 'registration/ViewVehicles.html'
    
    
class UpdateProfile(UpdateView):
    model = EndUserProfile
    fields = (
        'bio', 'user_id'
        )
    template_name = 'registration/UpdateProfile.html'
    # queryset = Profile.objects.all()

    
class DetailProfile(DetailView): 
    model = EndUserProfile
    exclude = []
    template_name = 'registration/DetailProfile.html' 
    context_object_name = 'profile_details'
    slug_field = "nickname"
    def get_queryset(self):
        return DetailView.get_queryset(self)
     
  
class TagList(ListView):
    model = Tag
    exclude = []
    template_name = 'registration/ViewTags.html'


class PrizeList(ListView):
    model = Prize
    exclude = []
    template_name = 'registration/ViewPrizes.html'
    
