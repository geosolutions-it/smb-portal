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





class Datapoint(models.Model):
    elevation = models.FloatField(blank=True, null=True)
    sessionid = models.BigIntegerField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)
    accelerationx = models.FloatField(blank=True, null=True)
    accelerationy = models.FloatField(blank=True, null=True)
    accelerationz = models.FloatField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    batconsumptionperhour = models.FloatField(blank=True, null=True)
    batterylevel = models.FloatField(blank=True, null=True)
    devicebearing = models.FloatField(blank=True, null=True)
    devicepitch = models.FloatField(blank=True, null=True)
    deviceroll = models.FloatField(blank=True, null=True)
    gps_bearing = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    lumen = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    proximity = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    vehiclemode = models.IntegerField(blank=True, null=True)
    serialversionuid = models.BigIntegerField(blank=True, null=True)
    color = models.BigIntegerField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_id = models.UUIDField(db_column='_id')  # Field renamed because it started with '_'.
    vehicle_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'datapoints'


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


class Tag(models.Model):
    epc = models.TextField(primary_key=True)
    vehicle = models.ForeignKey('Vehicles', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'tags'


class User(AbstractUser):
    username = models.TextField(primary_key=True)
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
        db_table = 'users'
        unique_together = (('username', 'sub'),)













    
    
    
# class PrizeManager(AbstractUser):
#     
#     email_address = models.CharField(max_length=100)
       

    



    
    
    

class receipt(models.Model):
    created_at= models.DateTimeField()
    owner_id = models.ForeignKey(User,on_delete=models.CASCADE)
    rfid_id = models.ForeignKey(Tag,on_delete=models.CASCADE)
    

    
    
    
    
class prize(models.Model):
    prize_id = models.AutoField(primary_key=True)
    prizemanager_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    #number_of_badges = models.IntegerField(0)
    
    
    

class Badge(models.Model):
    id = models.AutoField(primary_key = True)
    #prize_id = models.ForeignKey(prize, on_delete=models.CASCADE)
    number_of_badges = models.IntegerField()
    type_of_badge = models.CharField(max_length=100)
    
    
    
    
    











