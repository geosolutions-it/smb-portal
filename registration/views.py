from django.shortcuts import render
from django.views.generic import ListView
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

# class bikesList(APIView,ListView):
#     template_name = 'registration/ViewVehicle.html'
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = bikes.objects.all()
#         serializer = SnippetSerializer(bikes, many=True)
#         return Response(serializer.data)
# 
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
# class ViewRegisterVehicles(SingleObjectMixin,ListView,APIView):
#     template_name = 'registratin/ViewVehicles.html'
#     
#     
#     def get(self,request, *args, **kwargs):
#         self.object = self.get_object(queryset= Vehicle.objects.all())
#         return super().get(request,*args,**kwargs)
#     
#     
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Vehicle'] = self.object
#         return context
#     
#     
#     def get_queryset(self):
#         return self.object.book_set.all()
    
    