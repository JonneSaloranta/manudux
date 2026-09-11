from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Appliance, ApplianceDocument, Location, Property


class ApplianceDocumentViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")
        self.location = Location.objects.create(name="Kitchen", property=self.property)
        self.appliance = Appliance.objects.create(name="Fridge", location=self.location)
        self.document = ApplianceDocument.objects.create(
            name="Purchase receipt",
            appliance=self.appliance,
            file=SimpleUploadedFile("receipt.pdf", b"content", "application/pdf"),
        )

    @tag("views", "auth", "appliancedocument")
    def test_create_document_view_is_public(self):
        response = self.client.get(
            reverse(
                "manudux:create-appliance-document",
                kwargs={"appliance_pk": self.appliance.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "appliancedocument")
    def test_create_document(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:create-appliance-document",
                kwargs={"appliance_pk": self.appliance.pk},
            ),
            data={
                "name": "Warranty certificate",
                "category": "warranty",
                "file": SimpleUploadedFile(
                    "warranty.pdf", b"content", "application/pdf"
                ),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ApplianceDocument.objects.filter(
                name="Warranty certificate", appliance=self.appliance
            ).exists()
        )

    @tag("views", "auth", "appliancedocument")
    def test_appliance_detail_lists_documents(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:appliance", kwargs={"pk": self.appliance.pk})
        )
        self.assertContains(response, "Purchase receipt")

    @tag("views", "auth", "appliancedocument")
    def test_delete_document_confirmation_page(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse(
                "manudux:delete-appliance-document", kwargs={"pk": self.document.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/appliance-document-delete.html")

    @tag("views", "auth", "appliancedocument")
    def test_delete_document(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:delete-appliance-document", kwargs={"pk": self.document.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("manudux:appliance", kwargs={"pk": self.appliance.pk})
        )
        self.assertFalse(ApplianceDocument.objects.filter(pk=self.document.pk).exists())
