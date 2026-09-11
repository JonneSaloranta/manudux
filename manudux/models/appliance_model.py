from django.db import models
from django.utils.translation import gettext_lazy as _

from . import ApplianceType, Guide, Location


class Appliance(models.Model):
    """Represents a tracked appliance/asset at a location (e.g., a furnace, a fridge)."""

    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="appliances"
    )
    appliance_type = models.ForeignKey(
        ApplianceType,
        on_delete=models.SET_NULL,
        related_name="appliances",
        blank=True,
        null=True,
    )
    brand = models.CharField(max_length=255, blank=True)
    model_number = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_expires = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="appliances", blank=True, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)
    guest_visible = models.BooleanField(
        default=False,
        help_text=_("Show this appliance to anyone browsing with a guest code."),
    )

    def __str__(self):
        return f"{self.name} -> {self.location.name}"

    class Meta:
        verbose_name = _("Appliance")
        verbose_name_plural = _("Appliances")
