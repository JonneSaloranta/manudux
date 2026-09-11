from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from . import Guide, LocationType, Property


class Location(models.Model):
    """Represents a specific location within a property (e.g., garage, closet)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="locations/images/", blank=True, null=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="locations"
    )
    location_type = models.ForeignKey(
        LocationType,
        on_delete=models.SET_NULL,
        related_name="locations",
        blank=True,
        null=True,
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
        with transaction.atomic():
            if self.pk:  # If location already exists (update)
                old_instance = Location.objects.get(pk=self.pk)
                if (
                    old_instance.name != self.name
                    or old_instance.description != self.description
                    or old_instance.activated != self.activated
                ):
                    self.property.updated_at = now()
                    self.property.save(update_fields=["updated_at"])
            else:  # If creating a new location
                self.property.updated_at = now()
                self.property.save(update_fields=["updated_at"])

            super().save(*args, **kwargs)  # Call the original save method

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
