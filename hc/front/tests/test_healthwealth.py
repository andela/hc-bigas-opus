from hc.api.models import ExternalChecks
from hc.test import BaseTestCase


class HealthWealthFrontTestCase(BaseTestCase):
    def setUp(self):
        """Set up the tests variables"""
        super(HealthWealthFrontTestCase, self).setUp()
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

    def test_checks_renders_correct_status(self):
        """Test after running third party ping it visually updates check status"""
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-grace")

        # Mobile
        self.assertContains(r, "label-warning")
