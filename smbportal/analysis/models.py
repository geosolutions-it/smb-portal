from django.db import models
from smbportal.vehicles.models import Datapoint
from smbportal.registration.models import User
# Create your models here.


class Analyse(models.Model):
    Analyst = models.ForeignKey(User,on_delete=models.CASCADE)
    position = modelsForeignKey(Datapoint,on_delete=models.CASCADE)
    city = models.TextField()
    awards = models.ForeignKey(Prize,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,on_delete= models.CASCADE)
    time_period = models.TimeField()