from django.conf import settings

from .models.guestcode_model import GUEST_SESSION_KEY


def site_settings(request):
    """Expose select settings to every template."""
    return {
        "ALLOW_REGISTRATION": settings.ALLOW_REGISTRATION,
        "APP_VERSION": settings.APP_VERSION,
        "is_guest_session": bool(request.session.get(GUEST_SESSION_KEY)),
    }
