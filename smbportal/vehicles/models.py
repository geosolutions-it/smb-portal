from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gismodels


# TODO: decide how to integrate external tables that are used by other apps

class Vehicle(models.Model):
    # id = models.BigAutoField(primary_key=True)
    last_update = models.DateTimeField(
        auto_now=True,
        db_column="lastupdate",
    )
    last_position = models.ForeignKey(
        "Datapoint",
        models.DO_NOTHING,
        db_column='lastposition',
        blank=True,
        null=True
    )

    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    brand = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    status = models.IntegerField(
        blank=True,
        null=True
    )  # foreignkey to vehicle status
    image = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.DO_NOTHING,
        db_column='owner',
        blank=True,
        null=True
    )
    field_id = models.UUIDField(
        db_column='_id',
        blank=True,
        null=True
    )  # Field renamed because it started with '_'.

    class Meta:
        db_table = 'vehicles'
        managed = False


# TODO: Integrate django-photolog for bike picture gallery
class Bike(models.Model):
    RACING_BIKE = "racing"
    CITY_BIKE = "city"
    MOUNTAIN_BIKE = "mountain"
    FOLDABLE_BIKE = "foldable"

    SINGLE_RING_GEAR = "single ring"
    GROUPSET_UNDER_18_SPEED_GEAR = "groupset below 18 speeds"
    GROUPSET_ABOVE_18_SPEED_GEAR = "groupset above 18 speeds"
    ELECTRIC_GEAR = "electric"

    DISK_BRAKE = "disk"
    CANTILEVER_BRAKE = "cantilever"
    COASTER_BRAKE = "coaster"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE
    )
    type_ = models.CharField(
        max_length=20,
        choices=(
            (RACING_BIKE, RACING_BIKE),
            (CITY_BIKE, CITY_BIKE),
            (MOUNTAIN_BIKE, MOUNTAIN_BIKE),
            (FOLDABLE_BIKE, FOLDABLE_BIKE),
        ),
        default=CITY_BIKE,
    )
    brand = models.CharField(
        max_length=50,
        blank=True,
    )
    model = models.CharField(
        max_length=50,
        blank=True,
    )
    gear = models.CharField(
        max_length=50,
        choices=(
            (SINGLE_RING_GEAR, SINGLE_RING_GEAR),
            (GROUPSET_UNDER_18_SPEED_GEAR, GROUPSET_UNDER_18_SPEED_GEAR),
            (GROUPSET_ABOVE_18_SPEED_GEAR, GROUPSET_ABOVE_18_SPEED_GEAR),
            (ELECTRIC_GEAR, ELECTRIC_GEAR),
        ),
        default=GROUPSET_ABOVE_18_SPEED_GEAR,
    )
    brake = models.CharField(
        max_length=30,
        choices=(
            (DISK_BRAKE, DISK_BRAKE),
            (CANTILEVER_BRAKE, CANTILEVER_BRAKE),
            (COASTER_BRAKE, COASTER_BRAKE),
        ),
        default=DISK_BRAKE,
    )
    color = models.CharField(
        max_length="100",
        blank=True,
    )
    saddle = models.CharField(
        max_length=100,
        blank=True,
    )
    has_basket = models.BooleanField(default=False)
    has_cargo_rack = models.BooleanField(default=False)
    has_lights = models.BooleanField(default=False)
    has_bags = models.BooleanField(default=False)
    has_smb_sticker = models.BooleanField(
        default=False,
        verbose_name="has SaveMyBike sticker"
    )
    other_details = models.TextField()


class BikePossessionHistory(models.Model):
    WITH_OWNER = "with owner"
    LOST = "lost"
    STOLEN = "stolen"
    FOUND_BY_THIRD_PARTY = "found by third party"

    bike = models.ForeignKey(
        "Bike",
        models.CASCADE
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
    )
    possession_state = models.CharField(
        max_length=50,
        choices=(
            (WITH_OWNER, WITH_OWNER),
            (LOST, LOST),
            (STOLEN, STOLEN),
            (FOUND_BY_THIRD_PARTY, FOUND_BY_THIRD_PARTY),
        ),
        default=WITH_OWNER,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(
        blank=True
    )


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


class Datapoint(gismodels.Model):
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
    username = models.TextField(blank=True)
    field_id = models.UUIDField(db_column='_id')
    vehicle_id = models.UUIDField(blank=True, null=True)
    the_geom = gismodels.PointField()

    class Meta:
        db_table = 'datapoints'
        managed = False
