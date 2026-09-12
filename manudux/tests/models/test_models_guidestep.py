from django.contrib.auth.models import User
from django.test import Client, TestCase, tag

from manudux.models import Guide, GuideStep


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

        GuideStep.objects.create(
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
            test_guidestep.created_at, msg="created_at should not be None."
        )

    @tag("models", "guidestep")
    def test_guidestep_updated_at(self):
        """Test if the guide updated time works correctly."""
        test_guidestep = GuideStep.objects.get(title="Test Guide Step")
        self.assertIsNotNone(
            test_guidestep.updated_at, msg="updated_at should not be None."
        )

    @tag("models", "guidestep")
    def test_guidestep_str(self):
        """Test the string representation of the GuideStep."""
        test_guide = GuideStep.objects.get(title="Test Guide Step")

        # return f"Step {self.step_number} for {self.guide.name}"
        self.assertEqual(
            str(test_guide),
            "Step 1 for Test Guide Name",
            msg=f"The string representation should be 'Step 1 for Test Guide Name', but got '{test_guide!s}'",
        )

    @tag("models", "guidestep")
    def test_guidesteps_are_ordered_by_step_number(self):
        """Steps should come back ordered by step_number regardless of creation order"""
        guide = Guide.objects.get(name="Test Guide Name")

        GuideStep.objects.create(
            guide=guide, title="Third", step_number=3, description="c"
        )
        GuideStep.objects.create(
            guide=guide, title="Second", step_number=2, description="b"
        )

        step_numbers = list(guide.steps.values_list("step_number", flat=True))
        self.assertEqual(
            step_numbers,
            [1, 2, 3],
            msg=f"Steps should be ordered by step_number, got {step_numbers}",
        )
