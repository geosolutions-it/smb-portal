from django.contrib import admin
#from django.contrib.auth.models import User as original
from vehicles.models import Vehicle, VehicleType, Tag

from .models import User,Receipt, Prize
from profiles.models import Profile


admin.site.register(VehicleType)
admin.site.register(User)
#admin.site.register(original)
admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(Receipt)
admin.site.register(Tag)
admin.site.register(Prize)