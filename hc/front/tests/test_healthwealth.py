from hc.api.models import ExternalChecks, Check
from hc.test import BaseTestCase


class HealthWealthFrontTestCase(BaseTestCase):
    def setUp(self):
        """Set up the tests variables"""
        super(HealthWealthFrontTestCase, self).setUp()
        self.check = Check()
        self.external_check = ExternalChecks()
        self.external_check.save()

    def test_it_renders_page(self):
        """Test it renders the healthwealth page correctly"""
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/integrations/add_healthwealth/")
        self.assertEqual(r.status_code, 200)

        # Desktop
        self.assertContains(r, "Add your custom integrations with third party services")

        # Mobile
        self.assertContains(r, "Add your custom integrations with third party services")
