from bossoidc.admin import KeycloakInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
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
        "user_permissions",
        "last_login",
        "date_joined",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# boss-oidc already registered the user model
admin.site.unregister(get_user_model())
admin.site.register(models.SmbUser, SmbUserAdmin)
admin.site.register(models.EndUserProfile)
admin.site.register(models.MobilityHabitsSurvey)
