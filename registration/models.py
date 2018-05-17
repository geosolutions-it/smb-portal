from django.db import models
from django.conf import settings
from rest_framework import serializers
#import  user model from here
#--->
# Create your models here.
from django.contrib.auth.models  import AbstractUser





class EndUser(AbstractUser):
    
    #profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    given_name = models.CharField(max_length=100) 
    surname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    
# class PrizeManager(AbstractUser):
#     
#     email_address = models.CharField(max_length=100)
       
    
    
class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    date_created = models.DateField()
    date_updated = models.DateField()
    


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
    
    

class receipt(models.Model):
    created_at= models.DateTimeField()
    owner_id = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    

class Tag(models.Model):
    vehicle_id = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    Vehicle_type = models.CharField(max_length=100)
    

class bike(Vehicle):
    bikes_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length = 200)
    rfid_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #registration_date =models.ForeignKey(Receipt,on_delete=models.CASCADE)
    
    
    
    
class prize(models.Model):
    prize_id = models.AutoField(primary_key=True)
    prizemanager_id = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    
    
    


    
    
    
    
    











