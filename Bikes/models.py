from django.db import models
#import ugettext()

# Create your models here.

# users model
#Users must be able to register, signin, query , report bike 
class Users(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
    
   #
    registration_date = models.DateTimeField('date published')
    
    
    
