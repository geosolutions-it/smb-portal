from django.contrib import admin

from .models import EndUser,Profile,Vehicle,receipt,Tag,bike, prize

admin.site.register(EndUser)
admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(receipt)
admin.site.register(Tag)
admin.site.register(bike)
admin.site.register(prize)