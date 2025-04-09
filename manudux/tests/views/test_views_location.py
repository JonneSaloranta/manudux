from django.test import TestCase, tag, Client
from manudux.models import Property, Location
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class PropertyTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        Property.objects.create(
            name="Test Property",
            description="Test Description",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345",
            activated=True,
        )

        Property.objects.create(
            name="Test Property1",
            description="Test Description1",
            address="456 Test St",
            city="Test City1",
            state="Test State1",
            zip_code="54321",
            activated=True,
        )

        Property.objects.create(
            name="Test Property2",
            description="Test Description2",
            address="789 Test St",
            city="Test City2",
            state="Test State2",
            zip_code="13579",
            activated=True,
        )

        Property.objects.create(
            name="Test Property3",
            description="Test Description3",
            address="1098 Test St",
            city="Test City3",
            state="Test State3",
            zip_code="25467",
            activated=True,
        )

        Property.objects.create(
            name="Test Property4",
            description="Test Description4",
            address="321 Test St",
            city="Test City4",
            state="Test State4",
            zip_code="67890",
            activated=False,
        )

    @tag("views", "slow", "auth")
    def test_property_view_is_public(self):
        response = self.client.get(reverse("manudux:properties"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "slow", "auth")
    def test_property_view_is_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:properties"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("properties", response.context)

        properties = response.context["properties"]
        self.assertEqual(len(properties), 5)

    @tag("views", "slow", "auth")
    def test_property_detail_view_public(self):
        response = self.client.get(reverse("manudux:property", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "slow", "auth")
    def test_property_detail_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:property", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("property", response.context)

        property = response.context["property"]
        self.assertEqual(property.name, "Test Property")
        self.assertEqual(property.description, "Test Description")
