from django.test import TestCase, tag, Client
from manudux.models import Property, Location
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class PropertyTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
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

    @tag("views", "slow", "auth", "property")
    def test_property_view_is_public(self):
        """Test if logged out users are redirected to login page when trying to view properties"""
        response = self.client.get(reverse("manudux:properties"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "slow", "auth", "property")
    def test_property_view_is_private(self):
        """Test if logged in users can see properties"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:properties"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("properties", response.context)

        properties = response.context["properties"]
        self.assertEqual(len(properties), 5)

    @tag("views", "slow", "auth", "property")
    def test_property_detail_view_public(self):
        """Test if logged out users are redirected to login page when trying to view property"""
        response = self.client.get(reverse("manudux:property", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "slow", "auth", "property")
    def test_property_detail_view_when_authenticated(self):
        """Test if logged int users can view property details"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:property", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("property", response.context)

        property = response.context["property"]
        self.assertEqual(property.name, "Test Property")
        self.assertEqual(property.description, "Test Description")
        self.assertTemplateUsed(template_name="manudux/property.html")

    @tag("views", "slow", "auth", "property")
    def test_property_create_view_public(self):
        """Test if logged out users are redirected to login page when trying to create property"""
        response = self.client.get(reverse("manudux:create-property"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "slow", "auth", "property")
    def test_property_create_view_private(self):
        """Test if logged in users can access property creation page"""
        # Login a user
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("manudux:create-property"))
        self.assertEqual(response.status_code, 200)

    @tag("views", "slow", "auth", "property")
    def test_property_user_create_propery_object(self):
        self.client.login(username="testuser", password="testpassword")

        # check the starting number of properties
        pts = Property.objects.all()
        self.assertEqual(
            len(pts), 5, msg=f"There should be 5 properties but resulted in {len(pts)}"
        )

        # send a post request for creating a property
        property_data = {
            "name": "Test Property1111",
            "description": "Description",
            "address": "12345",
            "address": "Test Address",
            "city": "Test City",
            "state": "Test State",
            "zip_code": 12345,
        }

        response = self.client.post(
            reverse("manudux:create-property"), data=property_data
        )

        self.assertTrue(
            Property.objects.filter(name="Test Property1111").exists(),
            msg="Property was not created",
        )

        # check if the property was created in the database
        pts = Property.objects.all()
        self.assertEqual(
            len(pts), 6, msg=f"There should be 6 properties but resulted in {len(pts)}"
        )

        # check if user is being redirected
        self.assertEqual(response.status_code, 302, msg="User was not redirected")

        # check if the response url contains the property detail url
        self.assertTrue("property-detail", response.url)

        @tag("views", "slow", "auth", "property")
        def test_property_user_create_propery_object(self):
            self.client.login(username="testuser", password="testpassword")

            # delete all properties
            Property.objects.all().delete()

            property_data = {
                "name": "",
                "description": "Description",
                "address": "12345",
                "address": "Test Address",
                "city": "Test City",
                "state": "Test State",
                "zip_code": -12345,
            }

            response = self.client.post(
                reverse("manudux:create-property"), data=property_data
            )

            self.assertEqual(
                response.status_code,
                200,
                msg="User should have stayed on page for invalid data entry",
            )
            self.assertTrue(
                "form" in response.context, msg="No form context variable found"
            )

            form = response.context["form"]
            self.assertFormError(form, "name", "This field is required")
            self.assertFormError(
                form, "zip_code", "Zipcode should be a positive integer"
            )

            self.assertFalse(Property.objects.exists())
