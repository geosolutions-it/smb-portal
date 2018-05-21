from django.contrib import admin
#from django.contrib.auth.models import User
from vehicles.models import Vehicle, VehicleType

from .models import User,receipt,Tag, prize

admin.site.register(VehicleType)
#admin.site.register(EndUser)
#admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(receipt)
admin.site.register(Tag)
admin.site.register(prize)