from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag
from django.utils import timezone

from manudux.models import (
    Appliance,
    Location,
    MaintenanceLog,
    MaintenanceTask,
    Property,
)


class MaintenanceTaskTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tech", password="pw")
        self.property = Property.objects.create(name="Test Property")
        self.other_property = Property.objects.create(name="Other Property")
        self.location = Location.objects.create(name="Kitchen", property=self.property)
        self.appliance = Appliance.objects.create(name="Fridge", location=self.location)

    @tag("models", "maintenancetask")
    def test_mark_complete_on_recurring_task_advances_due_date(self):
        task = MaintenanceTask.objects.create(
            title="Clean filter",
            property=self.property,
            due_date=timezone.localdate() - timedelta(days=1),
            recurrence_interval_days=30,
        )

        task.mark_complete(self.user, notes="Done", cost=10)
        task.refresh_from_db()

        self.assertFalse(task.is_done)
        self.assertEqual(task.due_date, timezone.localdate() + timedelta(days=30))
        self.assertIsNotNone(task.last_completed_at)
        self.assertEqual(task.logs.count(), 1)

        log = task.logs.first()
        self.assertEqual(log.task_title, "Clean filter")
        self.assertEqual(log.completed_by, self.user)
        self.assertEqual(log.notes, "Done")
        self.assertEqual(log.cost, 10)

    @tag("models", "maintenancetask")
    def test_mark_complete_on_one_off_task_marks_it_done(self):
        task = MaintenanceTask.objects.create(
            title="Replace roof",
            property=self.property,
            due_date=timezone.localdate(),
        )

        task.mark_complete(self.user)
        task.refresh_from_db()

        self.assertTrue(task.is_done)
        self.assertEqual(
            task.due_date, timezone.localdate(), msg="one-off due_date should not move"
        )
        self.assertEqual(task.logs.count(), 1)

    @tag("models", "maintenancetask")
    def test_mark_complete_attaches_a_receipt(self):
        task = MaintenanceTask.objects.create(
            title="Replace filter",
            property=self.property,
            due_date=timezone.localdate(),
        )

        task.mark_complete(
            self.user,
            notes="Done",
            cost=25,
            receipt=SimpleUploadedFile("receipt.pdf", b"content", "application/pdf"),
        )

        log = task.logs.first()
        self.assertTrue(bool(log.receipt))
        self.assertIn("receipt", log.receipt.name)

    @tag("models", "maintenancetask")
    def test_mark_complete_without_a_receipt_is_still_optional(self):
        task = MaintenanceTask.objects.create(
            title="Replace filter",
            property=self.property,
            due_date=timezone.localdate(),
        )

        task.mark_complete(self.user)

        log = task.logs.first()
        self.assertFalse(bool(log.receipt))

    @tag("models", "maintenancetask")
    def test_log_survives_task_deletion(self):
        task = MaintenanceTask.objects.create(
            title="Clean gutters", property=self.property, due_date=timezone.localdate()
        )
        task.mark_complete(self.user)
        log_id = task.logs.first().id

        task.delete()

        log = MaintenanceLog.objects.get(pk=log_id)
        self.assertIsNone(log.task)
        self.assertEqual(log.task_title, "Clean gutters")
        self.assertIn(log, self.property.maintenance_logs.all())

    @tag("models", "maintenancetask")
    def test_clean_rejects_location_from_a_different_property(self):
        task = MaintenanceTask(
            title="Bad task",
            property=self.other_property,
            location=self.location,
            due_date=timezone.localdate(),
        )
        with self.assertRaises(ValidationError):
            task.clean()

    @tag("models", "maintenancetask")
    def test_clean_rejects_appliance_from_a_different_property(self):
        task = MaintenanceTask(
            title="Bad task",
            property=self.other_property,
            appliance=self.appliance,
            due_date=timezone.localdate(),
        )
        with self.assertRaises(ValidationError):
            task.clean()
