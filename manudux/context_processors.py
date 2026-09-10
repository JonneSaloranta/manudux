from django.conf import settings


def site_settings(request):
    """Expose select settings to every template."""
    return {
        "ALLOW_REGISTRATION": settings.ALLOW_REGISTRATION,
        "APP_VERSION": settings.APP_VERSION,
    }
