from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Guide, GuideFile


class GuideFileViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.guide = Guide.objects.create(name="Test Guide")
        self.guide_file = GuideFile.objects.create(
            name="Manual",
            guide=self.guide,
            file=SimpleUploadedFile("manual.pdf", b"content", "application/pdf"),
        )

    @tag("views", "auth", "guidefile")
    def test_create_guide_file_view_is_public(self):
        response = self.client.get(
            reverse("manudux:create-guide-file", kwargs={"guide_pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guidefile")
    def test_create_guide_file(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:create-guide-file", kwargs={"guide_pk": self.guide.pk}),
            data={
                "name": "Warranty",
                "file": SimpleUploadedFile(
                    "warranty.pdf", b"content", "application/pdf"
                ),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GuideFile.objects.filter(name="Warranty", guide=self.guide).exists()
        )

    @tag("views", "auth", "guidefile")
    def test_guide_detail_lists_files(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertContains(response, "Manual")

    @tag("views", "auth", "guidefile")
    def test_delete_guide_file_confirmation_page(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-guide-file", kwargs={"pk": self.guide_file.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/guide-file-delete.html")

    @tag("views", "auth", "guidefile")
    def test_delete_guide_file(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-guide-file", kwargs={"pk": self.guide_file.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertFalse(GuideFile.objects.filter(pk=self.guide_file.pk).exists())
