from django.db import models

# Create your models here.
class Badge(models.Model):
    id = models.AutoField(primary_key=True)
    number_of_badges = models.IntegerField()
    type_of_badge = models.CharField(max_length=100)
    number_of_miles = models.IntegerField()
    