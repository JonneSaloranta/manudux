from django.test import TestCase, tag, Client
from manudux.models.guide_model import Guide
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class GuideTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        guide = Guide.objects.create(
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
            test_guide.created_at, msg=f"The guide's created_at field is null"
        )

    @tag("models", "guide")
    def test_guide_updated_at(self):
        """Test if the updated_at works properly"""
        test_guide = Guide.objects.get(name="Test Guide Name")
        self.assertIsNotNone(
            test_guide.updated_at, msg=f"The guide's updated_at field is null"
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
