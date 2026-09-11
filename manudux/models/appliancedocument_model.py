from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Appliance
from ..validators import validate_appliance_document


class ApplianceDocument(models.Model):
    """A document attached to an appliance (receipt, warranty, manual, etc.)."""

    CATEGORY_RECEIPT = "receipt"
    CATEGORY_WARRANTY = "warranty"
    CATEGORY_MANUAL = "manual"
    CATEGORY_INSPECTION = "inspection"
    CATEGORY_OTHER = "other"
    CATEGORY_CHOICES = [
        (CATEGORY_RECEIPT, _("Receipt")),
        (CATEGORY_WARRANTY, _("Warranty")),
        (CATEGORY_MANUAL, _("Manual")),
        (CATEGORY_INSPECTION, _("Inspection report")),
        (CATEGORY_OTHER, _("Other")),
    ]

    appliance = models.ForeignKey(
        Appliance, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER
    )
    file = models.FileField(
        upload_to="appliances/documents/", validators=[validate_appliance_document]
    )
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.appliance.name})"

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("Appliance document")
        verbose_name_plural = _("Appliance documents")
