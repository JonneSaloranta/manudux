from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import MaintenanceTask, Property
from ..validators import validate_maintenance_receipt


class MaintenanceLog(models.Model):
    """A record that a maintenance task was completed."""

    task = models.ForeignKey(
        MaintenanceTask, on_delete=models.SET_NULL, null=True, related_name="logs"
    )
    task_title = models.CharField(max_length=255)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="maintenance_logs"
    )
    completed_at = models.DateTimeField(default=timezone.now)
    completed_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    notes = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    receipt = models.FileField(
        upload_to="maintenance/receipts/",
        blank=True,
        null=True,
        validators=[validate_maintenance_receipt],
    )

    def __str__(self):
        return f"{self.task_title} completed {self.completed_at:%Y-%m-%d}"

    class Meta:
        ordering = ["-completed_at"]
        verbose_name = _("Maintenance log")
        verbose_name_plural = _("Maintenance logs")
