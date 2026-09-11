from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag

from manudux.models import Appliance, ApplianceDocument, Location, Property


class ApplianceDocumentTestCase(TestCase):

    def setUp(self):
        self.property = Property.objects.create(name="Test Property")
        self.location = Location.objects.create(name="Kitchen", property=self.property)
        self.appliance = Appliance.objects.create(name="Fridge", location=self.location)

    @tag("models", "appliancedocument")
    def test_str(self):
        document = ApplianceDocument.objects.create(
            name="Purchase receipt",
            appliance=self.appliance,
            file=SimpleUploadedFile("receipt.pdf", b"content", "application/pdf"),
        )
        self.assertEqual(str(document), "Purchase receipt (Fridge)")

    @tag("models", "appliancedocument")
    def test_default_category_is_other(self):
        document = ApplianceDocument.objects.create(
            name="Misc",
            appliance=self.appliance,
            file=SimpleUploadedFile("misc.pdf", b"content", "application/pdf"),
        )
        self.assertEqual(document.category, ApplianceDocument.CATEGORY_OTHER)

    @tag("models", "appliancedocument")
    def test_rejects_disallowed_extension(self):
        document = ApplianceDocument(
            name="Script",
            appliance=self.appliance,
            file=SimpleUploadedFile(
                "payload.exe", b"content", "application/x-msdownload"
            ),
        )
        with self.assertRaises(ValidationError):
            document.full_clean()

    @tag("models", "appliancedocument")
    def test_deleted_when_appliance_deleted(self):
        document = ApplianceDocument.objects.create(
            name="Purchase receipt",
            appliance=self.appliance,
            file=SimpleUploadedFile("receipt.pdf", b"content", "application/pdf"),
        )
        self.appliance.delete()
        self.assertFalse(ApplianceDocument.objects.filter(pk=document.pk).exists())
