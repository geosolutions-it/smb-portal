from django.db import models
from registration.models import Datapoint
from profiles.models import  User
# Create your models here.
class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    type = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    lastposition = models.ForeignKey(Datapoint, models.DO_NOTHING, db_column='lastposition', blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner', blank=True, null=True)
    field_id = models.UUIDField(db_column='_id', blank=True, null=True)  # Field renamed because it started with '_'.
    #owner_0 = models.ForeignKey(Users, models.DO_NOTHING, db_column='owner_id', blank=True, null=True)  # Field renamed because of name conflict.

    class Meta:
        managed = True
        db_table = 'vehicles'
        
        
        

class VehilceStatus(models.Model):
    id = models.IntegerField()
    status = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)        

class VehicleType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vehicle_types'