from django.db import models
from smbportal.profiles.models import EndUserProfile
# Create your models here.

class Follower(models.Model):
    follower = models.ForeignKey(EndUserProfile,on_delete=models.CASCADE)
    followed_at = models.DateTimeField()
    
    
class Friend(models.Model):
    name = ForeignKey(EndUserProfile,on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    