from django.db import models
from django.conf import settings
from rest_framework import serializers


#import  user model from here
#--->
# Create your models here.
from django.contrib.auth.models  import AbstractUser
#from django.contrib.auth.models import User



# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models








class Position(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'positions'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'





class User(AbstractUser):
    username = models.TextField(unique = True)
    email = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    given_name = models.TextField(blank=True, null=True)
    family_name = models.TextField(blank=True, null=True)
    preferred_username = models.TextField(blank=True, null=True)
    cognito_user_status = models.NullBooleanField(db_column='cognito:user_status')  # Field renamed to remove unsuitable characters.
    status = models.TextField(blank=True, null=True)
    sub = models.TextField()
    id = models.BigAutoField(primary_key = True,unique=True)
    field_id = models.UUIDField(db_column='_id', unique=True, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = True
        db_table = 'user'
        unique_together = (('username', 'sub'),)





# for determining a user Habbits
class UserHabbits(models.Model):
    public_transportaion = models.IntegerField() # from least to most amount, 1 - 3
    customer_sharing = models.IntegerField()
    bicycle_usuage = models.IntegerField()
    


    
    
    

class Receipt(models.Model):
    created_at= models.DateTimeField()
    owner_id = models.ForeignKey(User,on_delete=models.CASCADE)
    #rfid_id = models.ForeignKey(Tag,on_delete=models.CASCADE)
    

    
    
    
    
class Prize(models.Model):
    prize_id = models.AutoField(primary_key=True)
    prizemanager_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    



    

class Badge(models.Model):
    id = models.AutoField(primary_key = True)
    number_of_badges = models.IntegerField()
    type_of_badge = models.CharField(max_length=100)
    
    
class PrizeandBadges(models.Model):
    id = models.AutoField(primary_key= True)
    prize_id = models.ForeignKey(Prize,on_delete=models.CASCADE)
    badge_id = models.ForeignKey(Badge,on_delete=models.CASCADE)
    
    
    
    
    











