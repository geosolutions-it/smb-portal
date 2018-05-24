from django.contrib import admin
from smbportal.vehicles.models import Vehicle, Tag
from smbportal.registration.models import Receipt
from smbportal.prizes.models import Prize
from smbportal.profiles.models import EndUserProfile
admin.site.register(Vehicle)
admin.site.register(Receipt)
admin.site.register(Tag)
admin.site.register(Prize)
admin.site.register(EndUserProfile)