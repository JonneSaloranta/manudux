from django.test import TestCase, tag, Client
from manudux.models import GuideStep, Guide
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class GuideStepTestCase(TestCase):

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

        guidestep = GuideStep.objects.create(
            guide=guide,
            title="Test Guide Step",
            step_number=1,
            description="This is a test step.",
        )

    @tag("models", "guidestep")
    def test_guidestep_title(self):
        """Test if the guide title works correctly"""
        test_guidestep = GuideStep.objects.get(title="Test Guide Step")
        self.assertEqual(
            test_guidestep.title,
            "Test Guide Step",
            msg=f"The guidestep title should be 'Test Guide Step', but got {test_guidestep.title}",
        )

    @tag("models", "guidestep")
    def test_guidestep_descriptiom(self):
        """Test if the guide description works correctly."""
        test_guidestep = GuideStep.objects.get(title="Test Guide Step")
        self.assertEqual(
            test_guidestep.description,
            "This is a test step.",
            msg=f"The guidestep description should be 'This is a test step.', but got {test_guidestep.description}",
        )

    @tag("models", "guidestep")
    def test_guidestep_created_at(self):
        """Test if the guide creationg time works correctly."""
        test_guidestep = GuideStep.objects.get(title="Test Guide Step")
        self.assertIsNotNone(
            test_guidestep.created_at, msg=f"created_at should not be None."
        )

    @tag("models", "guidestep")
    def test_guidestep_updated_at(self):
        """Test if the guide updated time works correctly."""
        test_guidestep = GuideStep.objects.get(title="Test Guide Step")
        self.assertIsNotNone(
            test_guidestep.updated_at, msg=f"updated_at should not be None."
        )

    @tag("models", "guidestep")
    def test_guidestep_str(self):
        """Test the string representation of the GuideStep."""
        test_guide = GuideStep.objects.get(title="Test Guide Step")

        # return f"Step {self.step_number} for {self.guide.name}"
        self.assertEqual(
            str(test_guide),
            "Step 1 for Test Guide Name",
            msg=f"The string representation should be 'Step 1 for Test Guide Name', but got '{str(test_guide)}'",
        )
