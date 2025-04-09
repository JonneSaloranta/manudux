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
from . import Property, Guide


class Location(models.Model):
    """Represents a specific location within a property (e.g., garage, closet)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="locations/images/", blank=True, null=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="locations"
    )
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        if self.property:
            return f"{self.name} -> {self.property.name}"
        else:
            return self.name

    def save(self, *args, **kwargs):
        """Update the property's updated_at field when a location is created or updated."""
        if self.pk:  # If location already exists (update)
            old_instance = Location.objects.get(pk=self.pk)
            if (
                old_instance.name != self.name
                or old_instance.description != self.description
                or old_instance.activated != self.activated
            ):
                self.property.updated_at = now()
                self.property.save()
        else:  # If creating a new location
            self.property.updated_at = now()
            self.property.save()

        super().save(*args, **kwargs)  # Call the original save method

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
