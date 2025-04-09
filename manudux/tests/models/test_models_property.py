from django.test import TestCase, tag, Client
from manudux.models.property_model import Property
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

    @tag("models", "property")
    def test_property_name(self):
        """Test if the property name works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.name,
            "Test Property",
            msg=f"The property name should be 'Test Property', but got {test_property.name}",
        )
        self.assertEqual(
            str(test_property),
            "Test Property",
            msg=f"The property name should be 'Test Property', but got {str(test_property)}",
        )

    @tag("models", "property")
    def test_property_description(self):
        """Test if the property description works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.description,
            "Test Description",
            msg=f"The property description should be 'Test Description', but got {test_property.description}",
        )

    @tag("models", "property")
    def test_property_address(self):
        """Test if the property address works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.address,
            "123 Test St",
            msg=f"The property address should be '123 Test St', but got {test_property.address}",
        )

    @tag("models", "property")
    def test_property_city(self):
        """Test if the property city works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.city,
            "Test City",
            msg=f"The property city should be 'Test City', but got {test_property.city}",
        )

    @tag("models", "property")
    def test_property_state(self):
        """Test if the property state works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.state,
            "Test State",
            msg=f"The property state should be 'Test State', but got {test_property.state}",
        )

    @tag("models", "property")
    def test_property_zip_code(self):
        """Test if the property zip code works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            test_property.zip_code,
            "12345",
            msg=f"The property zip code should be '12345', but got {test_property.zip_code}",
        )

    @tag("models", "property")
    def test_property_activated(self):
        """Test if the property activated works correctly"""
        activated_property = Property.objects.get(name="Test Property")
        self.assertEqual(
            activated_property.activated,
            True,
            msg=f"The property activated should be True, but got {activated_property.activated}",
        )

        deactivated_property = Property.objects.get(name="Test Property4")
        self.assertEqual(
            deactivated_property.activated,
            False,
            msg=f"The property activated should be False, but got {deactivated_property.activated}",
        )

    @tag("models", "property")
    def test_property_created_at(self):
        """Test if the property created at works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertIsNotNone(
            test_property.created_at,
            msg=f"The property created at should not be None, but got {test_property.created_at}",
        )

    @tag("models", "property")
    def test_property_updated_at(self):
        """Test if the property updated at works correctly"""
        test_property = Property.objects.get(name="Test Property")
        self.assertIsNotNone(
            test_property.updated_at,
            msg=f"The property updated at should not be None, but got {test_property.updated_at}",
        )

    @tag("models", "property")
    def test_if_property_zipcode_is_negative(self):
        """Test if negative property zipcode raises an valueerror"""
        pt = Property.objects.create(
            name="Property",
            description="testdescription",
            address="456 Test St",
            city="Test City2",
            state="Test State3",
            zip_code=-900,
            activated=True,
        )
        pt.save()
        self.assertRaises(
            ValueError,
            msg=f"The negative property zipcode should raise a ValueError, but did not",
        )

    @tag("models", "property")
    def test_if_get_map_function_works_correctly(self):
        """Test if property get_map function works"""
        pt = Property.objects.get(name="Test Property")
        self.assertIsNotNone(
            pt.get_map(), msg="The get_map function should not return None."
        )

        Property.objects.create(
            name="Test Property5",
            description="",
            address=None,
            city="Test City5",
            state="Test State5",
            zip_code="67890",
            activated=False,
        )

        pt = Property.objects.get(name="Test Property5")

        self.assertIsNone(
            pt.address, msg=f"The address should be None, returned {pt.address}"
        )
        self.assertIsNone(pt.get_map(), msg="The get_map function should return None.")

        pt.address = "321 Test St"
        pt.city = None
        pt.save()

        self.assertIsNone(pt.city, msg=f"The city should be None, returned {pt.city}")
        self.assertIsNone(pt.get_map(), msg="The get_map function should return None.")

        pt.city = "Test City5"
        pt.state = None
        pt.save()

        self.assertIsNone(
            pt.state, msg=f"The state should be None, returned {pt.state}"
        )
        self.assertIsNone(pt.get_map(), msg=f"The get_map function should return None")

        pt.state = "Test State5"
        pt.zip_code = None
        pt.save()
        self.assertIsNone(
            pt.zip_code, msg=f"The zipcode should be None, returned {pt.zip_code}"
        )
        self.assertIsNone(pt.get_map(), msg=f"The get_map function should return None")
