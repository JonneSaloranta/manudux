from django.test import TestCase, tag

from manudux.models import GuestCode, Property
from manudux.models.guestcode_model import CODE_LENGTH


class GuestCodeModelsTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(name="Test Property")

    @tag("models", "guestcode")
    def test_code_is_auto_generated_on_save(self):
        guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.assertEqual(len(guest_code.code), CODE_LENGTH)

    @tag("models", "guestcode")
    def test_generated_codes_are_unique(self):
        first = GuestCode.objects.create(name="Tenant A", property=self.property)
        second = GuestCode.objects.create(name="Tenant B", property=self.property)
        self.assertNotEqual(first.code, second.code)

    @tag("models", "guestcode")
    def test_code_is_not_regenerated_on_further_saves(self):
        guest_code = GuestCode.objects.create(name="Tenant A", property=self.property)
        original_code = guest_code.code
        guest_code.name = "Renamed tenant"
        guest_code.save()
        self.assertEqual(guest_code.code, original_code)

    @tag("models", "guestcode")
    def test_str(self):
        guest_code = GuestCode.objects.create(name="Tenant A", property=self.property)
        self.assertEqual(str(guest_code), "Tenant A (Test Property)")

    @tag("models", "guestcode")
    def test_deleted_when_property_deleted(self):
        guest_code = GuestCode.objects.create(name="Tenant A", property=self.property)
        self.property.delete()
        self.assertFalse(GuestCode.objects.filter(pk=guest_code.pk).exists())
