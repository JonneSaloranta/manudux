from django.test import TestCase, tag, Client
from manudux.models import Property, Location
from django.urls import reverse
from django.contrib.auth.models import User


class LocationViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.property = Property.objects.create(name="Test Property")

        self.location = Location.objects.create(
            name="Test Location",
            description="Test Description",
            property=self.property,
            activated=True,
        )

    @tag("views", "auth", "location")
    def test_locations_view_is_public(self):
        """Test if logged out users are redirected to login page when trying to view locations"""
        response = self.client.get(reverse("manudux:locations"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location")
    def test_locations_view_is_private(self):
        """Test if logged in users can see the locations list"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:locations"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("locations", response.context)
        self.assertEqual(len(response.context["locations"]), 1)

    @tag("views", "auth", "location")
    def test_location_detail_view_public(self):
        """Test if logged out users are redirected to login page when trying to view a location"""
        response = self.client.get(
            reverse("manudux:location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location")
    def test_location_detail_view_when_authenticated(self):
        """Test if logged in users can view a location's details"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("location", response.context)
        self.assertEqual(response.context["location"].name, "Test Location")
        self.assertTemplateUsed(response, "manudux/location.html")

    @tag("views", "auth", "location")
    def test_create_location_view_public(self):
        """Test if logged out users are redirected to login page when trying to create a location"""
        response = self.client.get(reverse("manudux:create-location"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location")
    def test_create_location_view_private(self):
        """Test if logged in users can create a location for a property"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:create-location"),
            data={
                "name": "New Location",
                "description": "New Description",
                "property": self.property.pk,
            },
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertTrue(Location.objects.filter(name="New Location").exists())

    @tag("views", "auth", "location")
    def test_edit_location_view_public(self):
        """Test if logged out users are redirected to login page when trying to edit a location"""
        response = self.client.get(
            reverse("manudux:edit-location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "location")
    def test_edit_location_view_private(self):
        """Test if logged in users can update a location"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:edit-location", kwargs={"pk": self.location.pk}),
            data={
                "name": "Updated Location",
                "description": "Updated Description",
                "property": self.property.pk,
            },
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Updated Location")
