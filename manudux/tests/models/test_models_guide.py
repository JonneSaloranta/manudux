from django.contrib.auth.models import User
from django.test import Client, TestCase, tag

from manudux.models.guide_model import Guide


class GuideTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        Guide.objects.create(
            name="Test Guide Name",
            description="This is a test guide.",
        )

    @tag("models", "guide")
    def test_guide_name(self):
        """Test if the guide name works correctly"""
        test_guide = Guide.objects.get(name="Test Guide Name")
        self.assertEqual(
            test_guide.name,
            "Test Guide Name",
            msg=f"The Guide name should be 'Test Guide Name', but got {test_guide.name}",
        )

    @tag("models", "guide")
    def test_guide_created_at(self):
        """Test if the created_at works properly"""
        test_guide = Guide.objects.get(name="Test Guide Name")
        self.assertIsNotNone(
            test_guide.created_at, msg="The guide's created_at field is null"
        )

    @tag("models", "guide")
    def test_guide_updated_at(self):
        """Test if the updated_at works properly"""
        test_guide = Guide.objects.get(name="Test Guide Name")
        self.assertIsNotNone(
            test_guide.updated_at, msg="The guide's updated_at field is null"
        )

    @tag("models", "guide")
    def test_guide_str(self):
        """Test the __str__ method of the Guide model"""
        test_guide = Guide.objects.get(name="Test Guide Name")
        self.assertEqual(
            f"{test_guide}",
            "Test Guide Name",
            msg=f"The guide name should be 'Test Guide Name', got {test_guide.name}",
        )

    @tag("models", "guide")
    def test_guide_qr_code_is_persisted_on_create(self):
        """save() generates a qr_code file, but previously never actually
        wrote it to the database for a brand-new guide (only to storage) -
        refetching the guide always came back with an empty qr_code."""
        test_guide = Guide.objects.get(name="Test Guide Name")
        refetched = Guide.objects.get(pk=test_guide.pk)
        self.assertTrue(
            bool(refetched.qr_code),
            msg="qr_code should be persisted to the database after create",
        )

    @tag("models", "guide")
    def test_guide_edit_persists_other_fields(self):
        """save() used to write only update_fields=["qr_code"] for an
        existing guide, silently discarding any other in-memory changes
        (e.g. a renamed guide)."""
        test_guide = Guide.objects.get(name="Test Guide Name")
        test_guide.name = "Renamed Guide"
        test_guide.save()
        refetched = Guide.objects.get(pk=test_guide.pk)
        self.assertEqual(refetched.name, "Renamed Guide")
