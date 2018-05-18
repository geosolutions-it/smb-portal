from django.contrib import admin
from django.contrib.auth.models import User

from .models import EndUser,Profile,Vehicles,receipt,Tag, prize,VehicleTypes

admin.site.register(VehicleTypes)
admin.site.register(EndUser)
admin.site.register(Profile)
admin.site.register(Vehicles)
admin.site.register(receipt)
admin.site.register(Tag)
admin.site.register(prize)