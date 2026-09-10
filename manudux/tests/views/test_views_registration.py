from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings, tag
from django.urls import reverse


class RegistrationViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    @tag("views", "auth", "registration")
    @override_settings(ALLOW_REGISTRATION=True)
    def test_signup_page_is_reachable_when_allowed(self):
        """Test that the signup page loads when ALLOW_REGISTRATION is True"""
        response = self.client.get(reverse("manudux:register"))
        self.assertEqual(response.status_code, 200)

    @tag("views", "auth", "registration")
    @override_settings(ALLOW_REGISTRATION=False)
    def test_signup_page_is_blocked_when_disallowed(self):
        """Test that the signup page is refused when ALLOW_REGISTRATION is False"""
        response = self.client.get(reverse("manudux:register"))
        self.assertEqual(response.status_code, 403)

    @tag("views", "auth", "registration")
    @override_settings(ALLOW_REGISTRATION=False)
    def test_signup_post_is_blocked_when_disallowed(self):
        """Test that posting to the signup page cannot create a user when disallowed"""
        response = self.client.post(
            reverse("manudux:register"),
            data={
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "S0mePassword!",
                "password2": "S0mePassword!",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    @tag("views", "auth", "registration")
    @override_settings(ALLOW_REGISTRATION=True)
    def test_login_page_shows_signup_link_when_allowed(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, reverse("manudux:register"))

    @tag("views", "auth", "registration")
    @override_settings(ALLOW_REGISTRATION=False)
    def test_login_page_hides_signup_link_when_disallowed(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertNotContains(response, reverse("manudux:register"))
