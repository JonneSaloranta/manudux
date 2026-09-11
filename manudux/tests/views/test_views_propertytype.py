from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import PropertyType


class PropertyTypeViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.property_type = PropertyType.objects.create(
            name="Residential", description="A place where you can live."
        )

    @tag("views", "auth", "property-type")
    def test_property_types_view_is_public(self):
        """Test if logged out users are redirected to login page when trying to view property types"""
        response = self.client.get(reverse("manudux:property-types"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "property-type")
    def test_property_types_view_is_private(self):
        """Test if logged in users can see the property types list"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:property-types"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("property_types", response.context)
        self.assertEqual(len(response.context["property_types"]), 1)

    @tag("views", "auth", "property-type")
    def test_create_property_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to create a property type"""
        response = self.client.get(reverse("manudux:create-property-type"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "property-type")
    def test_create_property_type_view_private(self):
        """Test if logged in users can create a property type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:create-property-type"),
            data={"name": "Commercial", "description": "A place where you can work."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertTrue(PropertyType.objects.filter(name="Commercial").exists())

    @tag("views", "auth", "property-type")
    def test_edit_property_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to edit a property type"""
        response = self.client.get(
            reverse("manudux:edit-property-type", kwargs={"pk": self.property_type.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "property-type")
    def test_edit_property_type_view_private(self):
        """Test if logged in users can update a property type"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("manudux:edit-property-type", kwargs={"pk": self.property_type.pk}),
            data={"name": "Updated Type", "description": "Updated description."},
        )

        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.property_type.refresh_from_db()
        self.assertEqual(self.property_type.name, "Updated Type")

    @tag("views", "auth", "property-type")
    def test_delete_property_type_view_public(self):
        """Test if logged out users are redirected to login page when trying to delete a property type"""
        response = self.client.get(
            reverse(
                "manudux:delete-property-type", kwargs={"pk": self.property_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "property-type")
    def test_delete_property_type_link_does_not_delete_immediately(self):
        """GET-ing the delete URL must render the confirmation page, not
        delete the property type - it should only be deleted on POST."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse(
                "manudux:delete-property-type", kwargs={"pk": self.property_type.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/property-type-delete.html")
        self.assertTrue(PropertyType.objects.filter(pk=self.property_type.pk).exists())

    @tag("views", "auth", "property-type")
    def test_delete_property_type_view_private(self):
        """Test if logged in users can delete a property type via POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:delete-property-type", kwargs={"pk": self.property_type.pk}
            )
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertFalse(PropertyType.objects.filter(pk=self.property_type.pk).exists())
