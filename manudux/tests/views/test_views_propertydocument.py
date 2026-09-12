from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Property, PropertyDocument


class PropertyDocumentViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")
        self.document = PropertyDocument.objects.create(
            name="Deed of sale",
            property=self.property,
            file=SimpleUploadedFile("deed.pdf", b"content", "application/pdf"),
        )

    @tag("views", "auth", "propertydocument")
    def test_create_document_view_is_public(self):
        response = self.client.get(
            reverse(
                "manudux:create-property-document",
                kwargs={"property_pk": self.property.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "propertydocument")
    def test_create_document(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:create-property-document",
                kwargs={"property_pk": self.property.pk},
            ),
            data={
                "name": "Insurance policy",
                "category": "insurance",
                "file": SimpleUploadedFile("policy.pdf", b"content", "application/pdf"),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            PropertyDocument.objects.filter(
                name="Insurance policy", property=self.property
            ).exists()
        )

    @tag("views", "auth", "propertydocument")
    def test_property_detail_lists_documents(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:property", kwargs={"pk": self.property.pk})
        )
        self.assertContains(response, "Deed of sale")

    @tag("views", "auth", "propertydocument")
    def test_delete_document_confirmation_page(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-property-document", kwargs={"pk": self.document.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/property-document-delete.html")

    @tag("views", "auth", "propertydocument")
    def test_delete_document(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-property-document", kwargs={"pk": self.document.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("manudux:property", kwargs={"pk": self.property.pk})
        )
        self.assertFalse(PropertyDocument.objects.filter(pk=self.document.pk).exists())
