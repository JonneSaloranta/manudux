from django.db import models
from django.utils.translation import gettext_lazy as _


class PropertyType(models.Model):
    """Represents a type of property (e.g., residential, commercial)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Property Type")
        verbose_name_plural = _("Property Types")
