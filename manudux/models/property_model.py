from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlencode
import textwrap
from django.conf import settings
import os
from . import PropertyType, Guide


class Property(models.Model):
    """Represents a property that can contain multiple locations."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="properties", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, blank=True, null=True)
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        related_name="properties",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_map(self):
        """Returns an embeddable Google Maps iframe for the property."""
        if not self.address or not self.city or not self.state or not self.zip_code:
            return None

        # Construct full address
        full_address = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"

        # URL encode the address for Google Maps
        params = urlencode({"q": full_address})

        # Generate the iframe with the dynamic address
        return (
            f'<div style="width: 100%;">'
            f'<iframe width="100%" height="400" frameborder="0" scrolling="no" '
            f'marginheight="0" marginwidth="0" '
            f'src="https://maps.google.com/maps?{params}&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed">'
            f"</iframe>"
            f"</div>"
        )

    def google_maps_link(self):
        """Generates a Google Maps link for the property's address."""
        if not self.address or not self.city or not self.state or not self.zip_code:
            return None  # Return None if the address is incomplete

        # Construct full address
        full_address = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"

        # URL encode the address
        params = urlencode({"q": full_address})

        return f"https://www.google.com/maps/search/?{params}"

    def zipcode_is_negative(self):
        if self.zip_code is None or "":
            return False
        else:
            if int(self.zip_code) < 0:
                raise ValueError(f"Zipcode cannot be negative {int(self.zip_code)}")
            else:
                return False

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
