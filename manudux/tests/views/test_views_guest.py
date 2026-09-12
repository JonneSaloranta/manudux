from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.urls import reverse

from manudux.models import Appliance, GuestCode, Guide, GuideStep, Location, Property


class GuestCodeManagementViewsTest(TestCase):
    """The owner-facing side: creating/revoking codes from the property page."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.property = Property.objects.create(name="Test Property")

    @tag("views", "auth", "guestcode")
    def test_create_guest_code_view_is_public(self):
        response = self.client.get(
            reverse(
                "manudux:create-guest-code", kwargs={"property_pk": self.property.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "auth", "guestcode")
    def test_create_guest_code(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse(
                "manudux:create-guest-code", kwargs={"property_pk": self.property.pk}
            ),
            data={"name": "3rd floor tenant"},
        )
        self.assertEqual(response.status_code, 302)
        guest_code = GuestCode.objects.get(name="3rd floor tenant")
        self.assertEqual(guest_code.property, self.property)
        self.assertEqual(guest_code.created_by, self.user)

    @tag("views", "auth", "guestcode")
    def test_property_detail_lists_guest_codes(self):
        GuestCode.objects.create(name="3rd floor tenant", property=self.property)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:property", kwargs={"pk": self.property.pk})
        )
        self.assertContains(response, "3rd floor tenant")

    @tag("views", "auth", "guestcode")
    def test_delete_guest_code_confirmation_page(self):
        guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("manudux:delete-guest-code", kwargs={"pk": guest_code.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manudux/guest-code-delete.html")
        self.assertTrue(GuestCode.objects.filter(pk=guest_code.pk).exists())

    @tag("views", "auth", "guestcode")
    def test_delete_guest_code(self):
        guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("manudux:delete-guest-code", kwargs={"pk": guest_code.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(GuestCode.objects.filter(pk=guest_code.pk).exists())


class GuestSessionViewsTest(TestCase):
    """The guest-facing side: logging in with a code and browsing read-only."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(
            name="Test Property",
            parcel_number="123-456-789",
            purchase_price=250000,
            insurance_company="Test Insurance Co",
        )
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.visible_location = Location.objects.create(
            name="Visible Location", property=self.property, guest_visible=True
        )
        self.hidden_location = Location.objects.create(
            name="Hidden Location", property=self.property, guest_visible=False
        )
        self.visible_appliance = Appliance.objects.create(
            name="Visible Appliance",
            location=self.visible_location,
            guest_visible=True,
        )
        self.hidden_appliance = Appliance.objects.create(
            name="Hidden Appliance",
            location=self.visible_location,
            guest_visible=False,
        )

    @tag("views", "guestcode")
    def test_guest_login_page_is_public(self):
        response = self.client.get(reverse("manudux:guest-login"))
        self.assertEqual(response.status_code, 200)

    @tag("views", "guestcode")
    def test_valid_code_starts_a_guest_session(self):
        response = self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        self.assertRedirects(response, reverse("manudux:guest-property"))
        self.assertEqual(self.client.session["guest_code_id"], self.guest_code.pk)

    @tag("views", "guestcode")
    def test_valid_code_is_case_insensitive(self):
        response = self.client.post(
            reverse("manudux:guest-login"),
            data={"code": self.guest_code.code.lower()},
        )
        self.assertRedirects(response, reverse("manudux:guest-property"))

    @tag("views", "guestcode")
    def test_invalid_code_does_not_start_a_session(self):
        response = self.client.post(
            reverse("manudux:guest-login"), data={"code": "NOTREAL1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("guest_code_id", self.client.session)

    @tag("views", "guestcode")
    def test_guest_property_view_without_a_session_redirects_to_login(self):
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertRedirects(response, reverse("manudux:guest-login"))

    @tag("views", "guestcode")
    def test_guest_view_shows_only_guest_visible_objects(self):
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Visible Location")
        self.assertContains(response, "Visible Appliance")
        self.assertNotContains(response, "Hidden Location")
        self.assertNotContains(response, "Hidden Appliance")

    @tag("views", "guestcode")
    def test_guest_view_excludes_financial_and_registry_fields(self):
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "123-456-789")
        self.assertNotContains(response, "250000")
        self.assertNotContains(response, "Test Insurance Co")

    @tag("views", "guestcode")
    def test_guest_session_cannot_reach_login_required_views(self):
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        response = self.client.get(reverse("manudux:properties"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("accounts/login" in response.url)

    @tag("views", "guestcode")
    def test_revoking_the_code_locks_out_the_guest_session(self):
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        self.guest_code.delete()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertEqual(response.status_code, 404)

    @tag("views", "guestcode")
    def test_guest_logout_clears_the_session(self):
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )
        self.client.post(reverse("manudux:guest-logout"))
        self.assertNotIn("guest_code_id", self.client.session)
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertRedirects(response, reverse("manudux:guest-login"))


class GuestGuideVisibilityTest(TestCase):
    """A guide's own guest_visible toggle, independent of the guest_visible
    flag on whatever property/location/appliance it's linked from."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(name="Test Property")
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.location = Location.objects.create(
            name="Visible Location", property=self.property, guest_visible=True
        )
        self.appliance = Appliance.objects.create(
            name="Visible Appliance", location=self.location, guest_visible=True
        )
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )

    def _make_guide(self, name, guest_visible):
        guide = Guide.objects.create(name=name, guest_visible=guest_visible)
        GuideStep.objects.create(
            guide=guide, step_number=1, title=f"{name} step", description="Do it."
        )
        return guide

    @tag("views", "guestcode")
    def test_hidden_location_guide_is_not_shown(self):
        self.location.guide = self._make_guide("Location guide", guest_visible=False)
        self.location.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "Location guide")

    @tag("views", "guestcode")
    def test_guest_visible_location_guide_is_shown(self):
        self.location.guide = self._make_guide("Location guide", guest_visible=True)
        self.location.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Manual: Location guide")

    @tag("views", "guestcode")
    def test_guide_link_renders_without_leaking_template_comments(self):
        """Regression test: a multi-line {# ... #} comment in a template
        isn't valid Django template syntax (it only works on a single
        line) - it silently falls through as literal text instead of
        raising an error, so this has to be caught by checking the
        rendered output rather than by a template syntax check."""
        self.location.guide = self._make_guide("Location guide", guest_visible=True)
        self.location.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "{#")
        self.assertNotContains(response, "#}")

    @tag("views", "guestcode")
    def test_hidden_appliance_guide_is_not_shown(self):
        self.appliance.guide = self._make_guide("Appliance guide", guest_visible=False)
        self.appliance.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "Appliance guide")

    @tag("views", "guestcode")
    def test_guest_visible_appliance_guide_is_shown(self):
        self.appliance.guide = self._make_guide("Appliance guide", guest_visible=True)
        self.appliance.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Manual: Appliance guide")

    @tag("views", "guestcode")
    def test_hidden_property_guide_is_not_shown(self):
        self.property.guide = self._make_guide("Property guide", guest_visible=False)
        self.property.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "Property guide")

    @tag("views", "guestcode")
    def test_guest_visible_property_guide_is_shown(self):
        self.property.guide = self._make_guide("Property guide", guest_visible=True)
        self.property.save()
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Manual: Property guide")


class GuestGuideDetailPageTest(TestCase):
    """The page a guide's link card on the property page points to, and
    the access control around it - a guest can only ever open a guide
    that's actually guest-visible on their own property."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(name="Test Property")
        self.other_property = Property.objects.create(name="Other Property")
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.location = Location.objects.create(
            name="Visible Location", property=self.property, guest_visible=True
        )
        self.guide = Guide.objects.create(name="Location guide", guest_visible=True)
        GuideStep.objects.create(
            guide=self.guide, step_number=1, title="Turn it off", description="."
        )
        self.location.guide = self.guide
        self.location.save()
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )

    @tag("views", "guestcode")
    def test_guide_page_shows_its_steps(self):
        response = self.client.get(
            reverse("manudux:guest-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Turn it off")

    @tag("views", "guestcode")
    def test_guide_page_requires_a_guest_session(self):
        self.client.post(reverse("manudux:guest-logout"))
        response = self.client.get(
            reverse("manudux:guest-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertRedirects(response, reverse("manudux:guest-login"))

    @tag("views", "guestcode")
    def test_guide_not_guest_visible_is_not_reachable(self):
        self.guide.guest_visible = False
        self.guide.save()
        response = self.client.get(
            reverse("manudux:guest-guide", kwargs={"pk": self.guide.pk})
        )
        self.assertEqual(response.status_code, 404)

    @tag("views", "guestcode")
    def test_guide_belonging_to_another_property_is_not_reachable(self):
        """A guest must not be able to view another customer's guide just
        by guessing its id, even if that guide is itself guest-visible."""
        other_location = Location.objects.create(
            name="Other Location", property=self.other_property, guest_visible=True
        )
        other_guide = Guide.objects.create(
            name="Other property's guide", guest_visible=True
        )
        other_location.guide = other_guide
        other_location.save()

        response = self.client.get(
            reverse("manudux:guest-guide", kwargs={"pk": other_guide.pk})
        )
        self.assertEqual(response.status_code, 404)


class GuestPropertySectionsTest(TestCase):
    """Sections of the guest property page only appear when there's
    something guest-visible to put in them, and a guest-visible appliance
    is never dropped just because its own location isn't guest-visible."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(name="Test Property")
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )

    @tag("views", "guestcode")
    def test_empty_property_shows_a_single_nothing_shared_message(self):
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Nothing has been shared with guests yet.")
        self.assertNotContains(response, "<h2>Locations</h2>", html=False)
        self.assertNotContains(response, "<h2>Appliances</h2>", html=False)

    @tag("views", "guestcode")
    def test_appliance_in_a_hidden_location_still_shows_up(self):
        """An appliance can be guest-visible even though the location it's
        in isn't (e.g. a shared laundry appliance in an otherwise private
        basement) - it must still reach the guest, in its own section."""
        hidden_location = Location.objects.create(
            name="Private Basement", property=self.property, guest_visible=False
        )
        Appliance.objects.create(
            name="Shared Washing Machine",
            location=hidden_location,
            guest_visible=True,
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Shared Washing Machine")
        self.assertContains(response, "Private Basement")
        self.assertNotContains(response, "Nothing has been shared with guests yet.")

    @tag("views", "guestcode")
    def test_appliance_in_a_visible_location_is_not_duplicated(self):
        """The same guest-visible appliance must not appear twice just
        because it would otherwise qualify for both the Locations and the
        standalone Appliances section."""
        visible_location = Location.objects.create(
            name="Visible Location", property=self.property, guest_visible=True
        )
        Appliance.objects.create(
            name="Visible Appliance", location=visible_location, guest_visible=True
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertEqual(response.content.decode().count("Visible Appliance"), 1)

    @tag("views", "guestcode")
    def test_locations_section_hidden_when_no_visible_locations(self):
        Location.objects.create(
            name="Hidden Location", property=self.property, guest_visible=False
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "<h2>Locations</h2>", html=False)

    @tag("views", "guestcode")
    def test_locations_and_appliances_render_as_collapsible_dropdowns(self):
        """Locations and appliances are <details> elements, collapsed by
        default, so a guest sees a compact list of names first and opens
        whichever one they actually need."""
        location = Location.objects.create(
            name="Visible Location", property=self.property, guest_visible=True
        )
        Appliance.objects.create(
            name="Visible Appliance", location=location, guest_visible=True
        )
        response = self.client.get(reverse("manudux:guest-property"))
        html = response.content.decode()
        self.assertIn('<details class="entity-list-item">', html)
        self.assertIn('<details class="detail-card">', html)
        # Collapsed by default - no bare "open" attribute on either tag.
        self.assertNotIn("<details open", html)


class GuestGuideDeduplicationTest(TestCase):
    """A guide can be attached to a property, one of its locations, and one
    of its appliances all at the same time (see attach_guide) - it must
    still only ever get one link card on the guest property page, shown at
    the most specific place it's encountered (appliance, then location,
    then property), not just wherever it happens to be visited first."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(name="Test Property")
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.guide = Guide.objects.create(name="Shared Guide", guest_visible=True)
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )

    def _card_count(self, response):
        return response.content.decode().count(f"/guest/guide/{self.guide.pk}/")

    @tag("views", "guestcode")
    def test_guide_attached_to_location_and_its_appliance_shows_once(self):
        location = Location.objects.create(
            name="Visible Location",
            property=self.property,
            guest_visible=True,
            guide=self.guide,
        )
        Appliance.objects.create(
            name="Visible Appliance",
            location=location,
            guest_visible=True,
            guide=self.guide,
        )
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertEqual(self._card_count(response), 1)
        self.assertContains(response, "Manual: Shared Guide", count=1)

    @tag("views", "guestcode")
    def test_shared_guide_nests_under_the_appliance_not_the_location(self):
        """Regression test: a guide attached to both a location and one of
        its own appliances (e.g. a water heater's own draining guide also
        linked from its "Varasto" location) must be shown once, under the
        appliance - not one level up, under the location, which is what a
        guest actually asked to see and what a naive top-down dedup pass
        got wrong (locations are visited before their appliances)."""
        location = Location.objects.create(
            name="Varasto",
            property=self.property,
            guest_visible=True,
            guide=self.guide,
        )
        Appliance.objects.create(
            name="LVV",
            location=location,
            guest_visible=True,
            guide=self.guide,
        )
        response = self.client.get(reverse("manudux:guest-property"))
        html = response.content.decode()
        self.assertEqual(self._card_count(response), 1)
        appliance_start = html.index('<details class="detail-card">')
        guide_link_index = html.index(f"/guest/guide/{self.guide.pk}/")
        self.assertGreater(
            guide_link_index,
            appliance_start,
            "guide link should be nested inside the appliance's own "
            "dropdown, not the location's",
        )

    @tag("views", "guestcode")
    def test_guide_attached_to_property_and_a_location_shows_once(self):
        self.property.guide = self.guide
        self.property.save()
        Location.objects.create(
            name="Visible Location",
            property=self.property,
            guest_visible=True,
            guide=self.guide,
        )
        response = self.client.get(reverse("manudux:guest-property"))
        html = response.content.decode()
        self.assertEqual(self._card_count(response), 1)
        # Claimed by the location, the more specific of the two - the card
        # must come after the Locations heading, not right under the
        # property header where the property-level card would sit.
        locations_heading_index = html.index("<h2>Locations</h2>")
        guide_link_index = html.index(f"/guest/guide/{self.guide.pk}/")
        self.assertGreater(guide_link_index, locations_heading_index)


class GuestNavigationTest(TestCase):
    """The owner-only navigation (Properties/Locations/Guides/Maintenance/
    Appliances menus and everything under them) must not be rendered for a
    guest session - those pages all 404/redirect-to-login for a guest
    anyway, so showing the links is just dead-end clutter, not a way in."""

    def setUp(self):
        self.client = Client()
        self.property = Property.objects.create(name="Test Property")
        self.guest_code = GuestCode.objects.create(
            name="3rd floor tenant", property=self.property
        )
        self.client.post(
            reverse("manudux:guest-login"), data={"code": self.guest_code.code}
        )

    @tag("views", "guestcode")
    def test_guest_view_hides_owner_only_navigation(self):
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertNotContains(response, "Create a new property")
        self.assertNotContains(response, "Manage appliance types")
        self.assertNotContains(response, "Add a task")
        self.assertNotContains(response, "Create a new guide")

    @tag("views", "guestcode")
    def test_guest_view_shows_guest_navigation(self):
        response = self.client.get(reverse("manudux:guest-property"))
        self.assertContains(response, "Exit guest view")
