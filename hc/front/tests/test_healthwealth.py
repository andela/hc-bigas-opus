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

    def test_checks_renders_correct_status(self):
        """Test after running third party ping it visually updates check status"""
        self.client.login(username="alice@example.org", password="password")
        self.client.post("/checks/add/")
        check = self.check.code
        form = {"third_party_url":"https://www.google.com/","check_url":"http://SITE_ROOT/ping/%s" % check,"name":"Google"}
        post_res = self.client.post("/integrations/add_healthwealth/", form)
        self.assertEqual(post_res.status_code, 200)
        check = ExternalChecks.objects.filter(check_url='http://SITE_ROOT/ping/%s' % check).first()
        res = self.client.get("/integrations/healthwealth_check/%s/" % check.id)
        self.assertEqual(res.status_code, 302)
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-up")
