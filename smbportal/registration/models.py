from django.db import models
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser
from django.db import models
from random import choices


public_transportation_choices = (
    (0,'normal (> 10 strokes / month), '),
    (1,'Light <10 strokes / month and> 10 rides / year),'),
    (2,'very sporadic (<10 strokes / year)')
    
    
    )

customer_sharing_choices = (
    (0,'bicycles'),
    (1,'electric cars'),
    (2,'fuell cars'),
    )

bicycle_usage_choices = (
    (0,'the usual (on average at least 1 time per week),'),
    (1,'socially (1 or more times a month), '),
    (2,'seasonal (mainly used in summer), '),
    (3,'sporadic (<12 times in a year),'),
    (4,'never to move in city.'),
    )
class Position(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'positions'


class User(AbstractUser):
    username = models.TextField(unique=True)
    email = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    given_name = models.TextField(blank=True, null=True)
    family_name = models.TextField(blank=True, null=True)
    preferred_username = models.TextField(blank=True, null=True)
    cognito_user_status = models.NullBooleanField(db_column='cognito:user_status')  # Field renamed to remove unsuitable characters.
    status = models.TextField(blank=True, null=True)
    sub = models.TextField()
    id = models.BigAutoField(primary_key=True, unique=True)
    field_id = models.UUIDField(db_column='_id', unique=True, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        unique_together = (('username', 'sub'),)


# for determining a user Habbits
class UserHabits(models.Model):
    public_transportaion = models.IntegerField(choices=public_transportation_choices)  # from least to most amount, 1 - 3
    customer_sharing = models.IntegerField(choices=customer_sharing_choices)
    bicycle_usuage = models.IntegerField()


class Receipt(models.Model):
    created_at= models.DateTimeField()
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    #rfid_id = models.ForeignKey(Tag,on_delete=models.CASCADE)









