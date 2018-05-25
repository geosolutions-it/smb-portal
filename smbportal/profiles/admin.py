from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class SmbUserAdmin(UserAdmin):
    pass


admin.site.register(models.SmbUser, SmbUserAdmin)
