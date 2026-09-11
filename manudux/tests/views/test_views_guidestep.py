from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Guide, GuideStep


class GuideStepViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.guide = Guide.objects.create(name="Test Guide")

        self.step = GuideStep.objects.create(
            guide=self.guide,
            step_number=1,
            title="First step",
            description="Do the first thing.",
        )

        self.second_step = GuideStep.objects.create(
            guide=self.guide,
            step_number=2,
            title="Second step",
            description="Do the second thing.",
        )

    @tag("views", "auth", "guidestep")
    def test_create_guide_step_view_public(self):
        response = self.client.get(
            reverse("manudux:create-guide-step", kwargs={"guide_pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guidestep")
    def test_create_guide_step_prefills_next_step_number(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:create-guide-step", kwargs={"guide_pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].initial["step_number"], 3)

    @tag("views", "auth", "guidestep")
    def test_create_guide_step_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:create-guide-step", kwargs={"guide_pk": self.guide.pk}),
            data={
                "step_number": 3,
                "title": "Third step",
                "description": "Do the third thing.",
            },
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertRedirects(
            response, reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        step = GuideStep.objects.get(title="Third step")
        self.assertEqual(step.guide, self.guide)

    @tag("views", "auth", "guidestep")
    def test_edit_guide_step_view_public(self):
        response = self.client.get(
            reverse("manudux:edit-guide-step", kwargs={"pk": self.step.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guidestep")
    def test_edit_guide_step_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:edit-guide-step", kwargs={"pk": self.step.pk}),
            data={
                "step_number": 1,
                "title": "Updated step",
                "description": "Updated description.",
            },
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.step.refresh_from_db()
        self.assertEqual(self.step.title, "Updated step")

    @tag("views", "auth", "guidestep")
    def test_delete_guide_step_link_does_not_delete_immediately(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-guide-step", kwargs={"pk": self.step.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/guide-step-delete.html")
        self.assertTrue(GuideStep.objects.filter(pk=self.step.pk).exists())

    @tag("views", "auth", "guidestep")
    def test_delete_guide_step_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-guide-step", kwargs={"pk": self.step.pk})
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertRedirects(
            response, reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertFalse(GuideStep.objects.filter(pk=self.step.pk).exists())

    @tag("views", "auth", "guidestep")
    def test_move_guide_step_view_public(self):
        response = self.client.get(
            reverse(
                "manudux:move-guide-step",
                kwargs={"pk": self.second_step.pk, "direction": "up"},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guidestep")
    def test_move_guide_step_up_swaps_with_previous(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:move-guide-step",
                kwargs={"pk": self.second_step.pk, "direction": "up"},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.step.refresh_from_db()
        self.second_step.refresh_from_db()
        self.assertEqual(self.second_step.step_number, 1)
        self.assertEqual(self.step.step_number, 2)

    @tag("views", "auth", "guidestep")
    def test_move_guide_step_down_swaps_with_next(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:move-guide-step",
                kwargs={"pk": self.step.pk, "direction": "down"},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.step.refresh_from_db()
        self.second_step.refresh_from_db()
        self.assertEqual(self.step.step_number, 2)
        self.assertEqual(self.second_step.step_number, 1)

    @tag("views", "auth", "guidestep")
    def test_move_first_step_up_is_a_noop(self):
        """There's no previous sibling for the first step - moving it up
        should not error, and nothing should change."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:move-guide-step",
                kwargs={"pk": self.step.pk, "direction": "up"},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.step.refresh_from_db()
        self.assertEqual(self.step.step_number, 1)

    @tag("views", "auth", "guidestep")
    def test_reorder_guide_steps_view_public(self):
        response = self.client.get(
            reverse("manudux:reorder-guide-steps", kwargs={"guide_pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guidestep")
    def test_reorder_guide_steps_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:reorder-guide-steps", kwargs={"guide_pk": self.guide.pk}),
            data={"step_id": [self.second_step.pk, self.step.pk]},
        )
        self.assertEqual(response.status_code, 302)
        self.step.refresh_from_db()
        self.second_step.refresh_from_db()
        self.assertEqual(self.second_step.step_number, 1)
        self.assertEqual(self.step.step_number, 2)
