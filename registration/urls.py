from django.urls import path
from rest_framework import serializers
from . import models
from rest_framework.routers import DefaultRouter
from registration import views
from django.conf.urls import url, include
from django.views.generic import TemplateView, CreateView, ListView
from .models import EndUser
router = DefaultRouter()
router.register(r'bikes', views.BikeViewSet)
router.register(r'prizes', views.PrizeViewSet)
router.register(r'Users',views.UserViewSet)

urlpatterns = [
    # ex: /polls/
    path('api/', include(router.urls)),
    path('newuser/', views.newuser.as_view(),name='newuser'),
    path('user/Vehicles',  views.vehicleList.as_view(),name='Vehicles'),
    path('user/Tags',views.TagList.as_view(),name='Tags'),
    path('user/updateProfile', views.UpdateProfile.as_view(),name='UpdateProfile'),
    path('user/DetailProfile/<slug:slug>/',views.DetailProfile.as_view(),name='DetailProfile'),
    path('home/',  TemplateView.as_view(template_name="registration/home.html"),name='home'),
    path('user/Prizes',views.PrizeList.as_view(),name='Prizes'),
    #path(r'single/', views.ViewRegisterVehicles.as_view(), name='index'),
    # ex: /polls/5/
   
]