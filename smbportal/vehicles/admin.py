from django.contrib import admin

from . import models


@admin.register(models.Bike)
class BikeAdmin(admin.ModelAdmin):
    pass
