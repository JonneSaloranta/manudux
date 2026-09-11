from django.test import TestCase, tag

from manudux.models import LocationType


class LocationTypeModelTest(TestCase):

    def setUp(self):

        LocationType.objects.create(name="Garage", description="A place to park a car.")
        LocationType.objects.create(
            name="Boiler Room", description="A place for the heating system."
        )
        LocationType.objects.create(
            name="Storage", description="A place to store things."
        )

    @tag("models", "LocationType")
    def test_location_type_name(self):
        """Verifies that the location type name is correct."""
        lt = LocationType.objects.get(name="Garage")
        self.assertEqual(
            lt.name, "Garage", msg="Location Type names should be the same"
        )
        self.assertEqual(
            str(lt),
            "Garage",
            msg=f"Location Type name should contain '{lt!s}', but got: {lt!s}",
        )
        self.assertEqual(
            lt.__str__(),
            "Garage",
            msg="Location Type names should be the same as str",
        )

    @tag("models", "LocationType")
    def test_location_type_description(self):
        """Verifies that the location type description is correct."""
        lt = LocationType.objects.get(name="Garage")
        self.assertEqual(
            lt.description,
            "A place to park a car.",
            msg=f"location type description is wrong. Should be:'{lt.description}'.",
        )

    @tag("models", "LocationType")
    def test_location_type_object_create(self):
        """Verifies that we can create a new location type object."""
        lts = LocationType.objects.all()
        self.assertEqual(
            len(lts),
            3,
            msg=f"There should be 3 location types but {len(lts)} was in the database.",
        )

        lt = LocationType.objects.create(
            name="Attic", description="A place to store seasonal items."
        )
        lt.save()
        lts = LocationType.objects.all()
        self.assertEqual(
            len(lts),
            4,
            msg=f"There should be 4 location types but {len(lts)} was in the database.",
        )

    @tag("models", "LocationType")
    def test_location_type_object_edit(self):
        """Verifies that we can edit a location type object."""
        lt = LocationType.objects.get(name="Garage")
        lt.name = "test-edit"
        lt.save()
        self.assertEqual(
            lt.name, "test-edit", msg="Location type names should be the same as str"
        )

    @tag("models", "LocationType")
    def test_location_type_object_delete(self):
        """Verifies that we can delete a location type object."""
        lt = LocationType.objects.get(name="Garage")
        lt.delete()
        lts = LocationType.objects.all()
        self.assertEqual(
            len(lts),
            2,
            msg=f"There should be 2 location types but got {len(lts)} in the database.",
        )

    @tag("models", "LocationType")
    def test_location_type_description_can_be_blank(self):
        """Verifies that a description can be blank."""
        lt = LocationType.objects.get(name="Boiler Room")
        lt.description = ""
        lt.save()
        self.assertIs(lt.description, "", msg="Description should be able to be blank.")

    @tag("models", "LocationType")
    def test_location_type_description_can_be_null(self):
        """Verifies that a description can be null."""
        lt = LocationType.objects.get(name="Boiler Room")
        lt.description = None
        lt.save()
        self.assertIsNone(lt.description, msg="Description should be able to be null.")
