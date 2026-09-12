from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from manudux.models import MaintenanceTask


class Command(BaseCommand):
    help = (
        "Email a digest of overdue and upcoming maintenance tasks to every "
        "active user with an email address. Intended to be run daily by an "
        "external cron/systemd timer."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the digest instead of sending any email.",
        )

    def handle(self, *args, **options):
        today = timezone.localdate()
        lookahead = today + timedelta(days=settings.MAINTENANCE_REMINDER_LOOKAHEAD_DAYS)

        active_tasks = MaintenanceTask.objects.filter(is_done=False).select_related(
            "property"
        )
        overdue = list(active_tasks.filter(due_date__lt=today))
        upcoming = list(
            active_tasks.filter(due_date__gte=today, due_date__lte=lookahead)
        )

        if not overdue and not upcoming:
            self.stdout.write("Nothing due or overdue - no reminders to send.")
            return

        body = self._build_digest(overdue, upcoming)
        recipients = User.objects.filter(is_active=True).exclude(email="")

        if options["dry_run"]:
            self.stdout.write(body)
            self.stdout.write(
                f"(dry run - would have emailed {recipients.count()} user(s))"
            )
            return

        sent = 0
        for user in recipients:
            send_mail(
                subject="Manudux maintenance reminders",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            sent += 1

        self.stdout.write(self.style.SUCCESS(f"Sent reminders to {sent} user(s)."))

    def _build_digest(self, overdue, upcoming):
        lines = []
        if overdue:
            lines.append("Overdue:")
            for task in overdue:
                lines.append(
                    f"  - {task.title} ({task.property.name}) - due {task.due_date}"
                )
        if upcoming:
            if lines:
                lines.append("")
            lines.append("Coming up:")
            for task in upcoming:
                lines.append(
                    f"  - {task.title} ({task.property.name}) - due {task.due_date}"
                )
        return "\n".join(lines)
