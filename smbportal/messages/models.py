from django.db import models

from smbportal.registration.models import User
from smbportal.profiles.models import Profile

# Create your models here.
class Message(models.Model):
    to_user = models.CharField(max_length=100)
    from_user = models.CharField(max_length=100)
    information = models.TextField()
    created_at = models.DateTimeField()


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    message = models.TextField()
    level_of_sharing = models.ForeignKey(Profile, on_delete=models.CASCADE)