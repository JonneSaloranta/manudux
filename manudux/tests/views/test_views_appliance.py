from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Appliance, Location, Property


class ApplianceViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")
        self.location = Location.objects.create(name="Kitchen", property=self.property)
        self.appliance = Appliance.objects.create(name="Fridge", location=self.location)

    @tag("views", "auth", "appliance")
    def test_appliances_view_is_public(self):
        response = self.client.get(reverse("manudux:appliances"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliance")
    def test_appliances_view_is_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:appliances"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("appliances", response.context)

    @tag("views", "auth", "appliance")
    def test_appliance_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:appliance", kwargs={"pk": self.appliance.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["appliance"].name, "Fridge")

    @tag("views", "auth", "appliance")
    def test_create_appliance_prefills_location(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            f"{reverse('manudux:create-appliance')}?location_id={self.location.pk}",
            data={
                "name": "Dishwasher",
                "location": self.location.pk,
                "activated": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Appliance.objects.filter(name="Dishwasher", location=self.location).exists()
        )

    @tag("views", "auth", "appliance")
    def test_edit_appliance(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:edit-appliance", kwargs={"pk": self.appliance.pk}),
            data={
                "name": "Fridge (updated)",
                "location": self.location.pk,
                "activated": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.appliance.refresh_from_db()
        self.assertEqual(self.appliance.name, "Fridge (updated)")

    @tag("views", "auth", "appliance")
    def test_delete_appliance(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-appliance", kwargs={"pk": self.appliance.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Appliance.objects.filter(pk=self.appliance.pk).exists())
