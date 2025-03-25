from django.test import TestCase
from .models import Property, Location

class PropertyTestCase(TestCase):
    def setUp(self):

    # name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='properties', blank=True, null=True)
    # address = models.CharField(max_length=255, blank=True, null=True)
    # city = models.CharField(max_length=255, blank=True, null=True)
    # state = models.CharField(max_length=255, blank=True, null=True)
    # zip_code = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # activated = models.BooleanField(default=True)

        Property.objects.create(name="Test Property", description="Test Description", address="123 Test St", city="Test City", state="Test State", zip_code="12345", activated=True)

    def test_property_name(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.name, 'Test Property')

    def test_property_description(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.description, 'Test Description')

    def test_property_address(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.address, '123 Test St')
    
    def test_property_city(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.city, 'Test City')

    def test_property_state(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.state, 'Test State')

    def test_property_zip_code(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.zip_code, '12345')

    def test_property_activated(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(test_property.activated, True)

    def test_property_created_at(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertIsNotNone(test_property.created_at)

    def test_property_updated_at(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertIsNotNone(test_property.updated_at)

    def test_property_str(self):
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(str(test_property), 'Test Property')

class LocationTestCase(TestCase):

    def setUp(self):
        
        # name = models.CharField(max_length=255)
        # description = models.TextField(blank=True, null=True)
        # property = models.ForeignKey(
        #     Property, on_delete=models.CASCADE, related_name='locations'
        # )
        # created_at = models.DateTimeField(auto_now_add=True)
        # updated_at = models.DateTimeField(auto_now=True)
        # activated = models.BooleanField(default=True)

        test_property = Property.objects.create(name="Test Property", description="Test Description", address="123 Test St", city="Test City", state="Test State", zip_code="12345", activated=True)
        Location.objects.create(name="Test Location", description="Test Description", property=test_property, activated=True)

    def test_location_name(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.name, 'Test Location')

    def test_location_description(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.description, 'Test Description')

    def test_location_property(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.property.name, 'Test Property')

    def test_location_activated(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(test_location.activated, True)

    def test_location_created_at(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertIsNotNone(test_location.created_at)

    def test_location_updated_at(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertIsNotNone(test_location.updated_at)

    def test_location_str(self):
        test_location = Location.objects.get(name="Test Location")
        self.assertEqual(str(test_location), 'Test Property - Test Location')

        