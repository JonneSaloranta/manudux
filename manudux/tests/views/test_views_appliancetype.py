from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import ApplianceType


class ApplianceTypeViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.appliance_type = ApplianceType.objects.create(
            name="HVAC", description="Heating and cooling."
        )

    @tag("views", "auth", "appliance-type")
    def test_appliance_types_view_is_public(self):
        """Test if logged out users are redirected to login page when trying to view appliance types"""
        response = self.client.get(reverse("manudux:appliance-types"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliance-type")
    def test_appliance_types_view_is_private(self):
        """Test if logged in users can see the appliance types list"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:appliance-types"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("appliance_types", response.context)
        self.assertEqual(len(response.context["appliance_types"]), 1)

    @tag("views", "auth", "appliance-type")
    def test_create_appliance_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to create an appliance type"""
        response = self.client.get(reverse("manudux:create-appliance-type"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliance-type")
    def test_create_appliance_type_view_private(self):
        """Test if logged in users can create an appliance type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:create-appliance-type"),
            data={"name": "Kitchen", "description": "Kitchen appliances."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertTrue(ApplianceType.objects.filter(name="Kitchen").exists())

    @tag("views", "auth", "appliance-type")
    def test_edit_appliance_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to edit an appliance type"""
        response = self.client.get(
            reverse(
                "manudux:edit-appliance-type", kwargs={"pk": self.appliance_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliance-type")
    def test_edit_appliance_type_view_private(self):
        """Test if logged in users can update an appliance type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse(
                "manudux:edit-appliance-type", kwargs={"pk": self.appliance_type.pk}
            ),
            data={"name": "Updated Type", "description": "Updated description."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.appliance_type.refresh_from_db()
        self.assertEqual(self.appliance_type.name, "Updated Type")

    @tag("views", "auth", "appliance-type")
    def test_delete_appliance_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to delete an appliance type"""
        response = self.client.get(
            reverse(
                "manudux:delete-appliance-type", kwargs={"pk": self.appliance_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliance-type")
    def test_delete_appliance_type_link_does_not_delete_immediately(self):
        """GET-ing the delete URL must render the confirmation page, not
        delete the appliance type - it should only be deleted on POST."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse(
                "manudux:delete-appliance-type", kwargs={"pk": self.appliance_type.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/appliance-type-delete.html")
        self.assertTrue(
            ApplianceType.objects.filter(pk=self.appliance_type.pk).exists()
        )

    @tag("views", "auth", "appliance-type")
    def test_delete_appliance_type_view_private(self):
        """Test if logged in users can delete an appliance type via POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:delete-appliance-type", kwargs={"pk": self.appliance_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertFalse(
            ApplianceType.objects.filter(pk=self.appliance_type.pk).exists()
        )
