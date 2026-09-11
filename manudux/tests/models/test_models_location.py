from django.test import TestCase, tag

from manudux.models import Location, LocationType, Property


class LocationModelsTest(TestCase):

    def setUp(self):

        test_property = Property.objects.create(
            name="Test Property",
            description="Test Description",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345",
            activated=True,
        )

        self.location_type = LocationType.objects.create(
            name="Garage", description="A place to park a car."
        )

        Location.objects.create(
            name="Test Location",
            description="Test Description",
            property=test_property,
            location_type=self.location_type,
            activated=True,
        )

    @tag("models", "Location")
    def test_location_name(self):
        """Tests for location name"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.name, "Test Location")

    @tag("models", "Location")
    def test_location_description(self):
        """Tests for location description"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.description, "Test Description")

    @tag("models", "Location")
    def test_location_property(self):
        """Tests for location property"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.property.name, "Test Property")

    @tag("models", "Location")
    def test_location_activated(self):
        """Tests for location activation"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.activated, True)

    @tag("models", "Location")
    def test_location_created_at(self):
        """Tests for location created at"""
        test_location = Location.objects.get(name="Test Location")
        self.assertIsNotNone(test_location.created_at)

    @tag("models", "Location")
    def test_location_updated_at(self):
        """Tests for location updated at"""
        test_location = Location.objects.get(name="Test Location")
        self.assertIsNotNone(test_location.updated_at)

    @tag("models", "Location")
    def test_location_str(self):
        """Tests for location string method"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(str(test_location), "Test Location -> Test Property")

    @tag("models", "Location")
    def test_location_type(self):
        """Tests that a location can be assigned a type"""
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.location_type.name, "Garage")

    @tag("models", "Location")
    def test_location_type_can_be_blank(self):
        """Tests that a location's type is optional"""
        test_property = Property.objects.get(name="Test Property")
        location = Location.objects.create(
            name="No Type Location", property=test_property
        )
        self.assertIsNone(location.location_type)

    @tag("models", "Location")
    def test_location_type_set_null_on_delete(self):
        """Deleting a LocationType should not delete the locations using it."""
        test_location = Location.objects.get(name="Test Location")
        self.location_type.delete()
        test_location.refresh_from_db()
        self.assertIsNone(test_location.location_type)
