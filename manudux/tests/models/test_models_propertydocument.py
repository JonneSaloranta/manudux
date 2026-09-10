from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag

from manudux.models import Property, PropertyDocument


class PropertyDocumentTestCase(TestCase):

    def setUp(self):
        self.property = Property.objects.create(name="Test Property")

    @tag("models", "propertydocument")
    def test_str(self):
        document = PropertyDocument.objects.create(
            name="Deed of sale",
            property=self.property,
            file=SimpleUploadedFile("deed.pdf", b"content", "application/pdf"),
        )
        self.assertEqual(str(document), "Deed of sale (Test Property)")

    @tag("models", "propertydocument")
    def test_default_category_is_other(self):
        document = PropertyDocument.objects.create(
            name="Misc",
            property=self.property,
            file=SimpleUploadedFile("misc.pdf", b"content", "application/pdf"),
        )
        self.assertEqual(document.category, PropertyDocument.CATEGORY_OTHER)

    @tag("models", "propertydocument")
    def test_rejects_disallowed_extension(self):
        document = PropertyDocument(
            name="Script",
            property=self.property,
            file=SimpleUploadedFile(
                "payload.exe", b"content", "application/x-msdownload"
            ),
        )
        with self.assertRaises(ValidationError):
            document.full_clean()

    @tag("models", "propertydocument")
    def test_deleted_when_property_deleted(self):
        document = PropertyDocument.objects.create(
            name="Deed of sale",
            property=self.property,
            file=SimpleUploadedFile("deed.pdf", b"content", "application/pdf"),
        )
        self.property.delete()
        self.assertFalse(PropertyDocument.objects.filter(pk=document.pk).exists())
