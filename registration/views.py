from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from registration.models import Vehicle, EndUser , bike, prize, Tag
from multiprocessing.sharedctypes import template
# Create your views here.
from rest_framework import serializers


#django-restfull framework
from registration.serializers import BikeSerializer, PrizeSerializer,UserSerializer,TagSerializer,ReceiptSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from django.views import generic


class BikeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = bike.objects.all()
    serializer_class = BikeSerializer
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
    success_url="registration/home/"
    
    
class vehicleList(ListView):
    model = bike
    #queryset = bike.objects.all(owner_id=request.user)
    fields = ('bikes_id','owner_id','model','created_at')
    template_name = 'registration/ViewVehicles.html'



    
    