from urllib.parse import urlencode

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Guide, PropertyType


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
        """Returns an embeddable Google Maps iframe src URL for the property.

        Building this as a URL rather than a chunk of HTML lets the template
        render the iframe itself, so it never needs the |safe filter.
        """
        if not self.address or not self.city or not self.state or not self.zip_code:
            return None

        # Construct full address
        full_address = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"

        # URL encode the address for Google Maps
        params = urlencode({"q": full_address})

        return f"https://maps.google.com/maps?{params}&t=&z=14&ie=UTF8&iwloc=B&output=embed"

    def google_maps_link(self):
        """Generates a Google Maps link for the property's address."""
        if not self.address or not self.city or not self.state or not self.zip_code:
            return None  # Return None if the address is incomplete

        # Construct full address
        full_address = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"

        # URL encode the address
        params = urlencode({"q": full_address})

        return f"https://www.google.com/maps/search/?{params}"

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
