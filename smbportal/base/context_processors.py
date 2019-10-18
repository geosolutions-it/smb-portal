from django.conf import settings


def global_settings(request):
    return {
        'SMB_PORTAL_MAINTENANCE_MESSAGE': settings.SMB_PORTAL_MAINTENANCE_MESSAGE,
    }