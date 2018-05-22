from django.contrib import admin
from smbportal.vehicles.models import Vehicle, Tag
from smbportal.registration.models import Receipt, Prize
admin.site.register(Vehicle)
admin.site.register(Receipt)
admin.site.register(Tag)
admin.site.register(Prize)
