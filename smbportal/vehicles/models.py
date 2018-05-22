from django.db import models
from smbportal.registration.models import User


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
        db_table = 'datapoints'


class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    brand = models.IntegerField(blank=True,null=True)
    type = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)# foreignkey to vehicle status
    lastposition = models.ForeignKey(Datapoint, models.DO_NOTHING, db_column='lastposition', blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner', blank=True, null=True)
    field_id = models.UUIDField(db_column='_id', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        db_table = 'vehicles'


class VehicleStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    class Meta:
        db_table = 'vehicle_status'


class VehicleType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'vehicle_types'


class Tag(models.Model):
    epc = models.TextField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)

    class Meta:
        db_table = 'tags'
