from hc.api.models import ExternalChecks, Check
from hc.front.forms import ExternalChecksForm
from hc.test import BaseTestCase
from time import sleep


class HealthWealthTestCase(BaseTestCase):
    def setUp(self):
        super(HealthWealthTestCase, self).setUp()
        self.check = Check()
        self.external_check = ExternalChecks()
        self.external_check.save()

    def test_user_can_create_integration(self):
        url = "/integrations/add_healthwealth/"
        self.client.login(username="alice@example.org", password="password")
        self.client.post("/checks/add/")
        test_check = "http://SITE_ROOT/ping/%s" % self.check.code
        test_form = {"third_party_url":"https://www.google.com/","check_url":test_check,"name":"Google"}
        r = self.client.post(url, test_form)
        self.assertEqual(r.status_code, 200)

        p = self.client.get("/checks/")
        self.assertContains(p, "icon-up")

    def test_user_can_delete_integration(self):
        """Test a user can delete an existing integration"""
        self.client.login(username="alice@example.org", password="password")
        self.client.post("/checks/add/")
        check = "http://SITE_ROOT/ping/%s" % self.check.code
        form = {"third_party_url":"https://www.google.com/","check_url":check,"name":"Google"}
        self.client.post("/integrations/add_healthwealth/", form)
        integration = ExternalChecks.objects.filter(check_url=check).first()
        initial_count = ExternalChecks.objects.count()
        r = self.client.post("/integrations/add_healthwealth/remove_integration/%s/" % integration.id, form)
        self.assertEqual(r.status_code, 302)
        assert ExternalChecks.objects.count() == initial_count - 1

    def test_the_integration_works(self):
        """Test a users integration can ping checks"""
        url = "/integrations/add_healthwealth/"
        self.client.login(username="alice@example.org", password="password")
        self.client.post("/checks/add/")
        test_check = "http://SITE_ROOT/ping/%s" % self.check.code

        r = self.client.get("/integrations/healthwealth_check/2/")
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, "/checks/")
