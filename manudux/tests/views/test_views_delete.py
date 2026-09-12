from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Location, Property


class DeleteConfirmationViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        self.property = Property.objects.create(
            name="Test Property",
            description="Test Description",
            activated=True,
        )

        self.location = Location.objects.create(
            name="Test Location",
            description="Test Description",
            property=self.property,
            activated=True,
        )

    @tag("views", "property", "delete")
    def test_property_delete_confirmation_page_renders(self):
        """GET on the property delete url should render a confirmation page, not 500"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-property", kwargs={"pk": self.property.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/property-delete.html")

    @tag("views", "property", "delete")
    def test_property_delete_post_deletes_object(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-property", kwargs={"pk": self.property.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Property.objects.filter(pk=self.property.pk).exists())

    @tag("views", "location", "delete")
    def test_location_delete_confirmation_page_renders(self):
        """GET on the location delete url should render a confirmation page, not 500"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/location-delete.html")

    @tag("views", "location", "delete")
    def test_location_delete_post_deletes_object(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-location", kwargs={"pk": self.location.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Location.objects.filter(pk=self.location.pk).exists())
