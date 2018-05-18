from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from registration.models import Vehicles, EndUser, prize, Tag, Profile
from multiprocessing.sharedctypes import template
# Create your views here.
from rest_framework import serializers


#django-restfull framework
from registration.serializers import VehicleSerializer, PrizeSerializer,UserSerializer,TagSerializer,ReceiptSerializer
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
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    template_name = 'registration/ViewVehicles.html'
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)



    def perform_create(self, serializer):
        serializer.save()
        

class PrizeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = prize.objects.all()
    serializer_class = PrizeSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)



    def perform_create(self, serializer):
        serializer.save()




class UserViewSet(viewsets.ModelViewSet):
    queryset = EndUser.objects.all()
    serializer_class = UserSerializer
    
    
    
    def perform_create(self, serializer):
        serializer.save()
        
        
        
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    
    def perform_create(self, serializer):
        serializer.save()
        
        
        
class newuser(CreateView):
    model = EndUser
    fields = ('username','password', 'first_name', 'last_name')
    exclude=[]
    template_name = 'registration/newuser.html'
    success_url="http://localhost:8000/registration/home/"
    
    
class vehicleList(ListView):
    model = Vehicles
    #queryset = bike.objects.all(owner_id=request.user)
    fields = ('bikes_id','owner_id','model','created_at')
    template_name = 'registration/ViewVehicles.html'
    
    
class UpdateProfile(UpdateView):
    model = Profile
    fields = ('bio','user_id')
    template_name = 'registration/UpdateProfile.html'
    #queryset = Profile.objects.all()
    
    
    
class TagList(ListView):
    model = Tag
    exclude=[]
    template_name = 'registration/ViewTags.html'

class PrizeList(ListView):
    model = prize
    exclude=[]
    template_name = 'registration/ViewPrizes.html'


    
    