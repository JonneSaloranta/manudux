from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import MaintenanceTask, Property


class MaintenanceTaskViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")
        self.task = MaintenanceTask.objects.create(
            title="Clean gutters",
            property=self.property,
            due_date=date.today() - timedelta(days=1),
            recurrence_interval_days=30,
        )

    @tag("views", "auth", "maintenance")
    def test_maintenance_tasks_view_is_public(self):
        response = self.client.get(reverse("manudux:maintenance-tasks"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "maintenance")
    def test_maintenance_tasks_default_filter_hides_done_tasks(self):
        MaintenanceTask.objects.create(
            title="Done task",
            property=self.property,
            due_date=date.today(),
            is_done=True,
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:maintenance-tasks"))
        titles = [t.title for t in response.context["maintenance_tasks"]]
        self.assertIn("Clean gutters", titles)
        self.assertNotIn("Done task", titles)

    @tag("views", "auth", "maintenance")
    def test_maintenance_tasks_overdue_filter(self):
        MaintenanceTask.objects.create(
            title="Future task",
            property=self.property,
            due_date=date.today() + timedelta(days=5),
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:maintenance-tasks"), {"filter": "overdue"}
        )
        titles = [t.title for t in response.context["maintenance_tasks"]]
        self.assertIn("Clean gutters", titles)
        self.assertNotIn("Future task", titles)

    @tag("views", "auth", "maintenance")
    def test_create_maintenance_task(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:create-maintenance-task"),
            data={
                "title": "New task",
                "property": self.property.pk,
                "due_date": date.today().isoformat(),
                "priority": "medium",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MaintenanceTask.objects.filter(title="New task").exists())

    @tag("views", "auth", "maintenance")
    def test_complete_maintenance_task_advances_due_date(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:maintenance-task", kwargs={"pk": self.task.pk}),
            data={"notes": "All good", "cost": "15.00"},
        )
        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()
        self.assertEqual(self.task.due_date, date.today() + timedelta(days=30))
        self.assertEqual(self.task.logs.count(), 1)

    @tag("views", "auth", "maintenance")
    def test_delete_maintenance_task(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-maintenance-task", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MaintenanceTask.objects.filter(pk=self.task.pk).exists())


class DashboardTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")
        self.overdue = MaintenanceTask.objects.create(
            title="Overdue task",
            property=self.property,
            due_date=date.today() - timedelta(days=5),
        )
        self.upcoming = MaintenanceTask.objects.create(
            title="Upcoming task",
            property=self.property,
            due_date=date.today() + timedelta(days=3),
        )
        self.far_future = MaintenanceTask.objects.create(
            title="Far future task",
            property=self.property,
            due_date=date.today() + timedelta(days=60),
        )

    @tag("views", "auth", "dashboard")
    def test_dashboard_hidden_for_anonymous_users(self):
        response = self.client.get(reverse("manudux:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("overdue_tasks", response.context)
        self.assertNotContains(response, "Overdue task")

    @tag("views", "auth", "dashboard")
    def test_dashboard_shows_overdue_and_upcoming_for_authenticated_users(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overdue task")
        self.assertContains(response, "Upcoming task")
        self.assertNotContains(response, "Far future task")
