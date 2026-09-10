from datetime import date, timedelta
from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings, tag
from django.contrib.auth.models import User

from manudux.models import Property, MaintenanceTask


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class SendMaintenanceRemindersTestCase(TestCase):

    def setUp(self):
        self.property = Property.objects.create(name="Test Property")

    @tag("management", "reminders")
    def test_no_tasks_sends_nothing(self):
        User.objects.create_user(username="a", password="pw", email="a@example.com")
        call_command("send_maintenance_reminders")
        self.assertEqual(len(mail.outbox), 0)

    @tag("management", "reminders")
    def test_sends_one_digest_per_active_user_with_an_email(self):
        MaintenanceTask.objects.create(
            title="Overdue task",
            property=self.property,
            due_date=date.today() - timedelta(days=1),
        )
        User.objects.create_user(username="a", password="pw", email="a@example.com")
        User.objects.create_user(username="b", password="pw", email="b@example.com")
        User.objects.create_user(username="no-email", password="pw", email="")
        User.objects.create_user(
            username="inactive", password="pw", email="c@example.com", is_active=False
        )

        call_command("send_maintenance_reminders")

        self.assertEqual(len(mail.outbox), 2)
        recipients = {r for message in mail.outbox for r in message.to}
        self.assertEqual(recipients, {"a@example.com", "b@example.com"})
        self.assertIn("Overdue task", mail.outbox[0].body)

    @tag("management", "reminders")
    def test_dry_run_sends_no_email(self):
        MaintenanceTask.objects.create(
            title="Overdue task",
            property=self.property,
            due_date=date.today() - timedelta(days=1),
        )
        User.objects.create_user(username="a", password="pw", email="a@example.com")

        out = StringIO()
        call_command("send_maintenance_reminders", "--dry-run", stdout=out)

        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("Overdue task", out.getvalue())
