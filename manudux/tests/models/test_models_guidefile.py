from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag

from manudux.models import Guide, GuideFile


class GuideFileTestCase(TestCase):

    def setUp(self):
        self.guide = Guide.objects.create(
            name="Test Guide Name",
            description="This is a test guide.",
        )

    @tag("models", "guidefile")
    def test_guidefile_accepts_allowed_extension(self):
        """A file with an allowed extension and size should validate fine"""
        guide_file = GuideFile(
            name="Manual",
            guide=self.guide,
            file=SimpleUploadedFile("manual.pdf", b"content", "application/pdf"),
        )
        guide_file.full_clean()  # should not raise

    @tag("models", "guidefile")
    def test_guidefile_rejects_disallowed_extension(self):
        """A file with a disallowed extension should fail validation"""
        guide_file = GuideFile(
            name="Script",
            guide=self.guide,
            file=SimpleUploadedFile("payload.exe", b"content", "application/x-msdownload"),
        )
        with self.assertRaises(ValidationError):
            guide_file.full_clean()

    @tag("models", "guidefile")
    def test_guidefile_rejects_oversized_file(self):
        """A file over the size limit should fail validation"""
        big_content = b"0" * (26 * 1024 * 1024)  # 26MB, over the 25MB limit
        guide_file = GuideFile(
            name="Big file",
            guide=self.guide,
            file=SimpleUploadedFile("manual.pdf", big_content, "application/pdf"),
        )
        with self.assertRaises(ValidationError):
            guide_file.full_clean()
