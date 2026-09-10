from django.test import Client, TestCase, tag
from django.urls import reverse


class HealthzViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    @tag("views", "healthz")
    def test_healthz_is_public_and_ok(self):
        """The health check should be reachable without auth and report ok"""
        response = self.client.get(reverse("healthz"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
