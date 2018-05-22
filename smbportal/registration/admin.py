from django.contrib import admin

from smbportal.profiles.models import Profile
from smbportal.vehicles.models import Vehicle, VehicleType, Tag

from .models import User, Receipt, Prize


admin.site.register(VehicleType)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(Receipt)
admin.site.register(Tag)
admin.site.register(Prize)
