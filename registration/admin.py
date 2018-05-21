from django.contrib import admin
#from django.contrib.auth.models import User

from .models import User,Profile,Vehicle,receipt,Tag, prize,VehicleType

admin.site.register(VehicleType)
#admin.site.register(EndUser)
admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(receipt)
admin.site.register(Tag)
admin.site.register(prize)