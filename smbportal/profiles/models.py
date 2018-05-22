from django.db import models


from django.contrib.auth.models  import AbstractUser
# Create your models here.

from smbportal.registration.models import User



class EndUserProfile(User):
    nickname = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
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





