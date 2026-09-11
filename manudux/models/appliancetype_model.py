from django.db import models
from django.utils.translation import gettext_lazy as _


class ApplianceType(models.Model):
    """Represents a type of appliance (e.g., HVAC, kitchen, water heater)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Appliance Type")
        verbose_name_plural = _("Appliance Types")
