from django.db import models

from django.contrib.auth.models  import AbstractUser
# Create your models here.


class EndUserProfile(AbstractUser):
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
    nickname = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=20)
    phone_number = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=200)
    date_created = models.DateField(blank=True, null=True)
    date_updated = models.DateField(blank=True, null=True)
    language_preference = models.IntegerField(blank=True, null=True)
    level_of_sharing = models.IntegerField(blank=True, null= True)
    profile_type = models.IntegerField(blank=True, null=True)
    profile_icon = models.CharField(max_length=200) 
    profile_name = models.CharField(max_length=200)
    
    class Meta:
        managed = True
        unique_together = (('username', 'sub'),)





    
    
