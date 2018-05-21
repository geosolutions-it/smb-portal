from django.db import models
from registration.models import User
# Create your models here.


#class EndUser(User):

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    bio = models.CharField(max_length=200)
    date_created = models.DateField()
    date_updated = models.DateField()
    language_preference = models.IntegerField()
    level_of_sharing = models.IntegerField(blank=True, null= True)
    class Meta:
        managed = True







class ProfileType(models.Model):
    profile_icon = models.CharField(max_length=200) 
    profile_name = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True)   
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    
