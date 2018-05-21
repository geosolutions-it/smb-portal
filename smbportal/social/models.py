from django.db import models

# Create your models here.

class Follower(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
    followed_at = models.DateTimeField()
    
    
class Friend(models.Model):
    name = ForeignKey(User,on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    