from django.test import TestCase, tag, Client
from manudux.models import Property, Location
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


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

        Location.objects.create(
            name="Test Location",
            description="Test Description",
            property=test_property,
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
