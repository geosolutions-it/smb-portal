from django.urls import path
from rest_framework import serializers
from . import models
from rest_framework.routers import DefaultRouter
from registration import views
from django.conf.urls import url, include


router = DefaultRouter()
router.register(r'bikes', views.BikeViewSet)
router.register(r'prizes', views.PrizeViewSet)
router.register(r'Users',views.UserViewSet)

urlpatterns = [
    # ex: /polls/
    path('api/', include(router.urls)),
    #path(r'single/', views.ViewRegisterVehicles.as_view(), name='index'),
    # ex: /polls/5/
   
]