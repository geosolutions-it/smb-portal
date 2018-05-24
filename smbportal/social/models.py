from django.db import models

from smbportal.registration.models import User
from smbportal.profiles.models import EndUserProfile

class Follower(models.Model):
    follower = models.ForeignKey(EndUserProfile, related_name = "follower",on_delete=models.CASCADE)
    creator = models.ForeignKey(User,related_name="creator",on_delete=models.CASCADE)
    followed_at = models.DateTimeField()


class Friend(models.Model):
    friend = models.ForeignKey(EndUserProfile,related_name="friend",on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="creator",on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
