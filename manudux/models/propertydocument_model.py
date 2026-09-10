from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Property
from ..validators import validate_property_document


class PropertyDocument(models.Model):
    """A document attached to a property (deed, insurance policy, etc.)."""

    CATEGORY_DEED = "deed"
    CATEGORY_INSURANCE = "insurance"
    CATEGORY_INSPECTION = "inspection"
    CATEGORY_FLOOR_PLAN = "floor_plan"
    CATEGORY_TAX = "tax"
    CATEGORY_WARRANTY = "warranty"
    CATEGORY_OTHER = "other"
    CATEGORY_CHOICES = [
        (CATEGORY_DEED, _("Deed")),
        (CATEGORY_INSURANCE, _("Insurance")),
        (CATEGORY_INSPECTION, _("Inspection report")),
        (CATEGORY_FLOOR_PLAN, _("Floor plan")),
        (CATEGORY_TAX, _("Tax")),
        (CATEGORY_WARRANTY, _("Warranty")),
        (CATEGORY_OTHER, _("Other")),
    ]

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER
    )
    file = models.FileField(
        upload_to="properties/documents/", validators=[validate_property_document]
    )
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.property.name})"

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("Property document")
        verbose_name_plural = _("Property documents")
