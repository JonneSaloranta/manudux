from django.test import TestCase, tag
from manudux.models import Property, Location, Appliance


class ApplianceTestCase(TestCase):

    def setUp(self):
        self.property = Property.objects.create(name="Test Property")
        self.location = Location.objects.create(name="Kitchen", property=self.property)

    @tag("models", "appliance")
    def test_appliance_str(self):
        appliance = Appliance.objects.create(name="Fridge", location=self.location)
        self.assertEqual(str(appliance), "Fridge -> Kitchen")

    @tag("models", "appliance")
    def test_appliance_defaults(self):
        appliance = Appliance.objects.create(name="Fridge", location=self.location)
        self.assertTrue(appliance.activated)
        self.assertEqual(appliance.brand, "")
        self.assertIsNone(appliance.purchase_date)

    @tag("models", "appliance")
    def test_appliance_deleted_when_location_deleted(self):
        appliance = Appliance.objects.create(name="Fridge", location=self.location)
        self.location.delete()
        self.assertFalse(Appliance.objects.filter(pk=appliance.pk).exists())
