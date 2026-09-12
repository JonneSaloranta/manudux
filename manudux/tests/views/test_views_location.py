from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Location, LocationType, Property


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

    @tag("views", "auth", "location")
    def test_create_location_view_accepts_a_type(self):
        """Test that a location can be created with a location type."""
        self.client.login(username="testuser", password="testpassword")
        location_type = LocationType.objects.create(name="Garage")

        response = self.client.post(
            reverse("manudux:create-location"),
            data={
                "name": "Garage Location",
                "property": self.property.pk,
                "location_type": location_type.pk,
            },
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        location = Location.objects.get(name="Garage Location")
        self.assertEqual(location.location_type, location_type)

    @tag("views", "auth", "location")
    def test_locations_view_only_shows_activated_locations(self):
        """Deactivated locations should not appear in the locations list."""
        Location.objects.create(
            name="Deactivated Location", property=self.property, activated=False
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:locations"))
        names = [location.name for location in response.context["locations"]]
        self.assertNotIn("Deactivated Location", names)
        self.assertIn("Test Location", names)

    @tag("views", "auth", "location")
    def test_delete_location_link_from_detail_page_does_not_delete_immediately(self):
        """GET-ing the delete URL (what the detail page's Delete button now
        links to) must render the confirmation page, not delete the
        location - it should only be deleted on POST."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/location-delete.html")
        self.assertTrue(Location.objects.filter(pk=self.location.pk).exists())
