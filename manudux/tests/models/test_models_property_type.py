from django.test import TestCase, tag, Client
from manudux.models import Property, Location, PropertyType
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class PropertyTypeModelTest(TestCase):

    # class PropertyType(models.Model):
    # """Represents a type of property (e.g., residential, commercial)."""
    # name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        PropertyType.objects.create(
            name="Residential", description="A place where you can live."
        )
        PropertyType.objects.create(
            name="Commercial", description="A place where you can work."
        )
        PropertyType.objects.create(
            name="Industrial", description="A place where you can work."
        )

    @tag("models", "PropertyType")
    def test_property_type_name(self):
        """Verifies that the property type name is correct."""
        pt = PropertyType.objects.get(name="Residential")
        self.assertEqual(
            pt.name, "Residential", msg="Property Type names should be the same"
        )
        self.assertEqual(
            str(pt),
            "Residential",
            msg=f"Property Type name should contain '{str(pt)}', but got: {str(pt)}",
        )
        self.assertEqual(
            pt.__str__(),
            "Residential",
            msg=f"Property Type names should be the same as str",
        )
        self.assertEqual(1, pt.id, msg=f"The property type should have an id of 1")

        pt = PropertyType.objects.get(id=1)
        self.assertEqual(
            pt.name,
            "Residential",
            msg=f"property type name has to be '{pt}' but got: {pt.name}.",
        )

    @tag("models", "PropertyType")
    def test_property_type_description(self):
        """Verifies that the property description is correct."""
        pt = PropertyType.objects.get(id=1)
        self.assertEqual(
            pt.description,
            "A place where you can live.",
            msg=f"property descrioption is wrong. Should be:'{pt.description}'.",
        )
        pt = PropertyType.objects.get(id=2)
        self.assertEqual(
            pt.description,
            "A place where you can work.",
            msg=f"property description is wrong. Should be: '{pt.description}'",
        )

    @tag("models", "PropertyType")
    def test_property_type_object_create(self):
        """Verifies that we can create a new property type object."""
        pts = PropertyType.objects.all()
        self.assertEqual(
            len(pts),
            3,
            msg=f"There should be 3 property types but {len(pts)} was in the database. ",
        )

        pt = PropertyType.objects.create(
            name="Test", description="A place where you can live."
        )
        pt.save()
        pts = PropertyType.objects.all()
        self.assertEqual(
            len(pts),
            4,
            msg=f"There should be 4 property types but {len(pts)} was in the database. There was an issue creating a property type",
        )

    @tag("models", "PropertyType")
    def test_property_type_object_edit(self):
        """Verifies that we can edit a property type object."""
        pt = PropertyType.objects.get(name="Residential")
        self.assertEqual(
            pt.description,
            "A place where you can live.",
            msg=f"property description is wrong.",
        )

        pt.name = "test-edit"
        pt.save()
        self.assertEqual(
            pt.name, "test-edit", msg=f"Property type names should be the same as str"
        )

    @tag("models", "PropertyType")
    def test_property_type_object_delete(self):
        """Verifies that we can delete a property type object."""
        pt = PropertyType.objects.get(name="Residential")
        pt.delete()
        pts: list[PropertyType] = PropertyType.objects.all()
        self.assertEqual(
            len(pts),
            2,
            msg=f"There should be 2 property types but got {len(pts)} in the database.",
        )

    @tag("models", "PropertyType")
    def test_property_type_description_can_be_blank(self):
        """Verifies that a description can be blank."""
        pt = PropertyType.objects.get(id=2)
        pt.description = ""
        pt.save()
        self.assertIs(pt.description, "", msg="Description should be able to be blank.")

    @tag("models", "PropertyType")
    def test_property_type_description_can_be_null(self):
        """Verifies that a description can be null."""
        pt = PropertyType.objects.get(id=2)
        pt.description = None
        pt.save()
        self.assertIsNone(pt.description, msg="Description should be able to be null.")
