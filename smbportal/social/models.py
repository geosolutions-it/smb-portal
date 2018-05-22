from django.db import models

from smbportal.registration.models import User

class Follower(models.Model):
    follower = models.ForeignKey(EndUserProfile,on_delete=models.CASCADE)
    followed_at = models.DateTimeField()


class Friend(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    created_at = models.DateTimeField()
