from django.db import models
from django.utils.translation import gettext_lazy as _


class LocationType(models.Model):
    """Represents a type of location within a property (e.g., garage, boiler room)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Location Type")
        verbose_name_plural = _("Location Types")
