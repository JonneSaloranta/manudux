from django.test import TestCase, tag, Client
from manudux.models import Property, Location
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class OtherViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

    @tag("views", "auth", "other")
    def test_index_page_public(self):
        """Test if logged out users can view the index page"""
        response = self.client.get(reverse("manudux:index"))
        self.assertEqual(response.status_code, 200)

    @tag("views", "auth", "other")
    def test_index_page_is_using_correct_template_when_authenticated(self):
        """Test if authenticated users can view the index page"""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("manudux:index"))

        self.assertEqual(
            response.status_code,
            200,
            msg="Index page should be served correctly when authenticated",
        )

        self.assertTemplateUsed(template_name="manudux/index.html")

    @tag("views", "auth", "other")
    def test_index_page_is_using_correct_template_when_logged_out(self):
        """Test if logged out users can view the index page"""
        response = self.client.get(reverse("manudux:index"))

        self.assertEqual(
            response.status_code,
            200,
            msg="Index page should be served correctly when not authenticated",
        )
        self.assertTemplateUsed(template_name="manudux/index.html")
