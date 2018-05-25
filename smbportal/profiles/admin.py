from bossoidc.admin import KeycloakInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required
from djangooidc.views import logout

from . import models


admin.site.login = login_required(admin.site.login)
admin.site.logout = logout


# TODO: prevent changing the keycloakinline fields too
# TODO: add admin classes for user profiles (those should allow editing)

class SmbUserAdmin(UserAdmin):
    inlines = (
        KeycloakInline,
    )
    readonly_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser",
        "is_staff",
        "groups",
        "last_login",
        "date_joined",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.SmbUser, SmbUserAdmin)
