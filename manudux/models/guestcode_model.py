import secrets
import string

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Property

# The session key a guest login writes and every guest-only view reads back.
# Shared as a constant (rather than a repeated string literal) between
# views.py and context_processors.py so the two can't drift apart.
GUEST_SESSION_KEY = "guest_code_id"

# Ambiguous characters (0/O, 1/I/L) are left out so a code stays easy to
# read aloud, hand-write, or copy from a note without misreads.
CODE_ALPHABET = "".join(
    c for c in string.ascii_uppercase + string.digits if c not in "0O1IL"
)
CODE_LENGTH = 8


def generate_guest_code():
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))


class GuestCode(models.Model):
    """A short code that grants a read-only, browser-session-only guest view
    of one property's guest-visible locations/appliances - never a real
    User account. What a code actually exposes is controlled by
    Location.guest_visible / Appliance.guest_visible on the objects
    themselves, not by anything on GuestCode."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="guest_codes"
    )
    name = models.CharField(
        max_length=255,
        help_text=_("Who this code was given to, e.g. a tenant's name."),
    )
    code = models.CharField(max_length=CODE_LENGTH, unique=True, editable=False)
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            code = generate_guest_code()
            while GuestCode.objects.filter(code=code).exists():
                code = generate_guest_code()
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.property.name})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Guest code")
        verbose_name_plural = _("Guest codes")
