from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import Appliance, Location, Property


class MaintenanceTask(models.Model):
    """A schedulable unit of maintenance work against a property/location/appliance."""

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _("Low")),
        (PRIORITY_MEDIUM, _("Medium")),
        (PRIORITY_HIGH, _("High")),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="maintenance_tasks"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="maintenance_tasks",
    )
    appliance = models.ForeignKey(
        Appliance,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="maintenance_tasks",
    )
    recurrence_interval_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "Leave blank for a one-off task. Otherwise, the number of days "
            "between occurrences, e.g. 30 for monthly."
        ),
    )
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    is_done = models.BooleanField(default=False)
    last_completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.property.name})"

    def clean(self):
        if self.location_id and self.location.property_id != self.property_id:
            raise ValidationError(
                {
                    "location": _(
                        "The selected location does not belong to this property."
                    )
                }
            )
        if (
            self.appliance_id
            and self.appliance.location.property_id != self.property_id
        ):
            raise ValidationError(
                {
                    "appliance": _(
                        "The selected appliance does not belong to this property."
                    )
                }
            )

    def mark_complete(self, user, notes="", cost=None, receipt=None):
        """Log a completion and, for recurring tasks, roll the due date forward."""
        from . import MaintenanceLog

        now = timezone.now()
        with transaction.atomic():
            MaintenanceLog.objects.create(
                task=self,
                task_title=self.title,
                property=self.property,
                completed_at=now,
                completed_by=user,
                notes=notes,
                cost=cost,
                receipt=receipt,
            )
            self.last_completed_at = now
            if self.recurrence_interval_days:
                # localdate(), not now.date(): due_date should roll forward
                # based on "today" in the configured TIME_ZONE, not the UTC
                # calendar date, which can differ for hours around midnight.
                self.due_date = timezone.localdate() + timedelta(
                    days=self.recurrence_interval_days
                )
            else:
                self.is_done = True
            self.save(
                update_fields=["last_completed_at", "due_date", "is_done", "updated_at"]
            )

    class Meta:
        ordering = ["due_date"]
        verbose_name = _("Maintenance task")
        verbose_name_plural = _("Maintenance tasks")
