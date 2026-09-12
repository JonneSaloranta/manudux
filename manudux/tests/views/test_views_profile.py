from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse


class ProfileViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )

    @tag("views", "auth", "profile")
    def test_profile_view_requires_login(self):
        response = self.client.get(reverse("manudux:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "profile")
    def test_profile_view_shows_own_data(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].instance, self.user)

    @tag("views", "auth", "profile")
    def test_profile_update_edits_own_account(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:profile"),
            data={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.email, "updated@example.com")

    @tag("views", "auth", "profile")
    def test_profile_update_does_not_affect_other_users(self):
        """The profile view has no pk in the URL - it should only ever be
        able to edit request.user, never another account."""
        self.client.login(username="testuser", password="testpassword")
        self.client.post(
            reverse("manudux:profile"),
            data={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
            },
        )
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.first_name, "")
