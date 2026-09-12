from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Appliance, Guide, GuideFile, Location, Property


class GuideViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        self.guide = Guide.objects.create(
            name="Test Guide", description="A guide used for testing."
        )

    @tag("views", "auth", "guide")
    def test_guide_list_view_requires_login(self):
        """The guide list must not be reachable while logged out."""
        response = self.client.get(reverse("manudux:guides"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_guide_list_view_when_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manudux:guides"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("guides", response.context)
        self.assertEqual(len(response.context["guides"]), 1)

    @tag("views", "auth", "guide")
    def test_guide_detail_view_requires_login(self):
        """The guide detail page (and therefore its QR code target) must
        not be reachable while logged out."""
        response = self.client.get(
            reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_guide_detail_view_when_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["guide"], self.guide)

    @tag("views", "auth", "guide")
    def test_create_guide_view_public(self):
        response = self.client.get(reverse("manudux:create-guide"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_create_guide_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:create-guide"),
            data={"name": "New Guide", "description": "New Description"},
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertTrue(Guide.objects.filter(name="New Guide").exists())

    @tag("views", "auth", "guide")
    def test_edit_guide_view_public(self):
        response = self.client.get(
            reverse("manudux:edit-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_edit_guide_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:edit-guide", kwargs={"pk": self.guide.pk}),
            data={"name": "Updated Guide", "description": "Updated Description"},
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.guide.refresh_from_db()
        self.assertEqual(self.guide.name, "Updated Guide")

    @tag("views", "auth", "guide")
    def test_delete_guide_link_does_not_delete_immediately(self):
        """GET-ing the delete URL must render the confirmation page, not
        delete the guide - it should only be deleted on POST."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/guide-delete.html")
        self.assertTrue(Guide.objects.filter(pk=self.guide.pk).exists())

    @tag("views", "auth", "guide")
    def test_delete_guide_view_private(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertFalse(Guide.objects.filter(pk=self.guide.pk).exists())

    @tag("views", "auth", "guide")
    def test_delete_guide_with_attached_file_succeeds(self):
        """GuideFile.guide is on_delete=PROTECT - deleting a guide that
        still has a file attached must not raise ProtectedError."""
        GuideFile.objects.create(
            name="Manual.pdf",
            guide=self.guide,
            file=SimpleUploadedFile("manual.pdf", b"content", "application/pdf"),
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        self.assertFalse(Guide.objects.filter(pk=self.guide.pk).exists())

    @tag("views", "auth", "guide")
    def test_attach_guide_view_public(self):
        response = self.client.get(
            reverse("manudux:attach-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_attach_guide_to_property(self):
        property_obj = Property.objects.create(name="Test Property")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:attach-guide", kwargs={"pk": self.guide.pk}),
            data={"property": property_obj.pk},
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        property_obj.refresh_from_db()
        self.assertEqual(property_obj.guide, self.guide)

    @tag("views", "auth", "guide")
    def test_attach_guide_to_location_and_appliance_together(self):
        property_obj = Property.objects.create(name="Test Property")
        location = Location.objects.create(name="Test Location", property=property_obj)
        appliance = Appliance.objects.create(name="Test Appliance", location=location)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:attach-guide", kwargs={"pk": self.guide.pk}),
            data={"location": location.pk, "appliance": appliance.pk},
        )
        self.assertEqual(response.status_code, 302, msg="User was not redirected")
        location.refresh_from_db()
        appliance.refresh_from_db()
        self.assertEqual(location.guide, self.guide)
        self.assertEqual(appliance.guide, self.guide)

    @tag("views", "auth", "guide")
    def test_attach_guide_requires_at_least_one_target(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:attach-guide", kwargs={"pk": self.guide.pk}), data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["attach_form"].is_valid())
        self.assertFalse(GuideFile.objects.filter(guide_id=self.guide.pk).exists())

    @tag("views", "auth", "guide")
    def test_detach_guide_view_requires_login(self):
        property_obj = Property.objects.create(name="Test Property", guide=self.guide)
        response = self.client.get(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "property",
                    "target_pk": property_obj.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guide")
    def test_detach_guide_confirmation_page(self):
        property_obj = Property.objects.create(name="Test Property", guide=self.guide)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "property",
                    "target_pk": property_obj.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/guide-detach-confirm.html")
        property_obj.refresh_from_db()
        self.assertEqual(property_obj.guide, self.guide, msg="Nothing detached yet")

    @tag("views", "auth", "guide")
    def test_detach_guide_from_property(self):
        property_obj = Property.objects.create(name="Test Property", guide=self.guide)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "property",
                    "target_pk": property_obj.pk,
                },
            )
        )
        self.assertRedirects(
            response, reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        property_obj.refresh_from_db()
        self.assertIsNone(property_obj.guide)

    @tag("views", "auth", "guide")
    def test_detach_guide_from_location_and_appliance(self):
        property_obj = Property.objects.create(name="Test Property")
        location = Location.objects.create(
            name="Test Location", property=property_obj, guide=self.guide
        )
        appliance = Appliance.objects.create(
            name="Test Appliance", location=location, guide=self.guide
        )
        self.client.login(username="testuser", password="testpassword")

        self.client.post(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "location",
                    "target_pk": location.pk,
                },
            )
        )
        self.client.post(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "appliance",
                    "target_pk": appliance.pk,
                },
            )
        )
        location.refresh_from_db()
        appliance.refresh_from_db()
        self.assertIsNone(location.guide)
        self.assertIsNone(appliance.guide)

    @tag("views", "auth", "guide")
    def test_detach_guide_rejects_unknown_model(self):
        property_obj = Property.objects.create(name="Test Property", guide=self.guide)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "not-a-real-model",
                    "target_pk": property_obj.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 404)

    @tag("views", "auth", "guide")
    def test_detach_guide_404s_if_not_actually_attached(self):
        """A guide can't be detached from something it isn't currently
        the manual for - e.g. a stale link, or a mismatched pk/model."""
        property_obj = Property.objects.create(name="Test Property")
        other_guide = Guide.objects.create(name="Other Guide")
        property_obj.guide = other_guide
        property_obj.save()
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "property",
                    "target_pk": property_obj.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 404)
        property_obj.refresh_from_db()
        self.assertEqual(property_obj.guide, other_guide)

    @tag("views", "guide")
    def test_guide_detail_shows_remove_link_for_used_by_items(self):
        property_obj = Property.objects.create(name="Test Property", guide=self.guide)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:guide", kwargs={"pk": self.guide.pk})
        )
        self.assertContains(
            response,
            reverse(
                "manudux:detach-guide",
                kwargs={
                    "guide_pk": self.guide.pk,
                    "model": "property",
                    "target_pk": property_obj.pk,
                },
            ),
        )
