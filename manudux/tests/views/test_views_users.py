from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse


class UsersViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpassword", email="admin@example.com"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpassword", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regularuser", password="regularpassword"
        )

    @tag("views", "auth", "users")
    def test_users_view_requires_login(self):
        response = self.client.get(reverse("manudux:users"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "users")
    def test_users_view_forbidden_for_non_superuser(self):
        """Even a staff user (but not a superuser) must not be able to
        manage other accounts - this is more sensitive than is_staff-gated
        pages like site-settings."""
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(reverse("manudux:users"))
        self.assertEqual(response.status_code, 403)

    @tag("views", "auth", "users")
    def test_users_view_forbidden_for_regular_user(self):
        self.client.login(username="regularuser", password="regularpassword")
        response = self.client.get(reverse("manudux:users"))
        self.assertEqual(response.status_code, 403)

    @tag("views", "auth", "users")
    def test_users_view_allowed_for_superuser(self):
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse("manudux:users"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)

    @tag("views", "auth", "users")
    def test_create_user_forbidden_for_non_superuser(self):
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(reverse("manudux:create-user"))
        self.assertEqual(response.status_code, 403)

    @tag("views", "auth", "users")
    def test_create_user_as_superuser(self):
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(
            reverse("manudux:create-user"),
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "S0mePassword!",
                "password2": "S0mePassword!",
                "is_staff": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username="newuser")
        self.assertTrue(new_user.is_staff)
        self.assertTrue(
            self.client.login(username="newuser", password="S0mePassword!"),
            msg="the new account should be able to log in with the password it was created with",
        )

    @tag("views", "auth", "users")
    def test_edit_user_forbidden_for_non_superuser(self):
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(
            reverse("manudux:edit-user", kwargs={"pk": self.regular_user.pk})
        )
        self.assertEqual(response.status_code, 403)

    @tag("views", "auth", "users")
    def test_edit_user_updates_role_and_active_status(self):
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(
            reverse("manudux:edit-user", kwargs={"pk": self.regular_user.pk}),
            data={
                "username": "regularuser",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": "on",
                "is_active": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_staff)
        self.assertFalse(self.regular_user.is_active)

    @tag("views", "auth", "users")
    def test_superuser_cannot_deactivate_or_destaff_themself(self):
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(
            reverse("manudux:edit-user", kwargs={"pk": self.superuser.pk}),
            data={
                "username": "admin",
                "first_name": "",
                "last_name": "",
                "email": "admin@example.com",
                "is_staff": "",
                "is_active": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.superuser.refresh_from_db()
        self.assertTrue(
            self.superuser.is_staff,
            msg="a superuser must not be able to remove their own staff access here",
        )
        self.assertTrue(
            self.superuser.is_active,
            msg="a superuser must not be able to deactivate themself here",
        )
