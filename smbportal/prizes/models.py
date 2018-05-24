from django.db import models
from smbportal.registration.models import User
from smbportal.badges.models import Badge
# Create your models here.
class Prize(models.Model):
    prize_id = models.AutoField(primary_key=True)
    prizemanager_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
class PrizeandBadges(models.Model):
    id = models.AutoField(primary_key= True)
    prize_id = models.ForeignKey(Prize,on_delete=models.CASCADE)
    badge_id = models.ForeignKey(Badge,on_delete=models.CASCADE)