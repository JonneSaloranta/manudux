from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import LocationType


class LocationTypeViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.location_type = LocationType.objects.create(
            name="Garage", description="A place to park a car."
        )

    @tag("views", "auth", "location-type")
    def test_location_types_view_is_public(self):
        """Test if logged out users are redirected to login page when trying to view location types"""
        response = self.client.get(reverse("manudux:location-types"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location-type")
    def test_location_types_view_is_private(self):
        """Test if logged in users can see the location types list"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:location-types"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("location_types", response.context)
        self.assertEqual(len(response.context["location_types"]), 1)

    @tag("views", "auth", "location-type")
    def test_create_location_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to create a location type"""
        response = self.client.get(reverse("manudux:create-location-type"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location-type")
    def test_create_location_type_view_private(self):
        """Test if logged in users can create a location type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:create-location-type"),
            data={"name": "Boiler Room", "description": "For the heating system."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertTrue(LocationType.objects.filter(name="Boiler Room").exists())

    @tag("views", "auth", "location-type")
    def test_edit_location_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to edit a location type"""
        response = self.client.get(
            reverse("manudux:edit-location-type", kwargs={"pk": self.location_type.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location-type")
    def test_edit_location_type_view_private(self):
        """Test if logged in users can update a location type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:edit-location-type", kwargs={"pk": self.location_type.pk}),
            data={"name": "Updated Type", "description": "Updated description."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.location_type.refresh_from_db()
        self.assertEqual(self.location_type.name, "Updated Type")

    @tag("views", "auth", "location-type")
    def test_delete_location_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to delete a location type"""
        response = self.client.get(
            reverse(
                "manudux:delete-location-type", kwargs={"pk": self.location_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location-type")
    def test_delete_location_type_link_does_not_delete_immediately(self):
        """GET-ing the delete URL must render the confirmation page, not
        delete the location type - it should only be deleted on POST."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse(
                "manudux:delete-location-type", kwargs={"pk": self.location_type.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/location-type-delete.html")
        self.assertTrue(LocationType.objects.filter(pk=self.location_type.pk).exists())

    @tag("views", "auth", "location-type")
    def test_delete_location_type_view_private(self):
        """Test if logged in users can delete a location type via POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:delete-location-type", kwargs={"pk": self.location_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertFalse(LocationType.objects.filter(pk=self.location_type.pk).exists())
