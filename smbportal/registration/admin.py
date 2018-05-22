from django.contrib import admin
from smbportal.vehicles.models import Vehicle, VehicleType, Tag

from .models import Receipt, Prize
from smbportal.profiles.models import EndUserProfile


admin.site.register(VehicleType)
admin.site.register(EndUserProfile)
admin.site.register(Vehicle)
admin.site.register(Receipt)
admin.site.register(Tag)
admin.site.register(Prize)