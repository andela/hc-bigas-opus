from hc.api.models import ExternalChecks, Check
from hc.front.forms import ExternalChecksForm
from hc.test import BaseTestCase


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
        print(test_check)

        test_form = {"third_party_url":"https://www.google.com/","check_url":test_check,"name":"Google"}
        r = self.client.post(url, test_form)
        print(r)
        self.assertEqual(r.status_code, 200)

    def test_user_can_delete_integration(self):
        """Test a user can delete an existing integration"""
        self.client.login(username="alice@example.org", password="password")
        self.client.post("/checks/add/")
        check = "http://SITE_ROOT/ping/%s" % self.check.code
        form = {"third_party_url":"https://www.google.com/","check_url":check,"name":"Google"}
        p = self.client.post("/integrations/add_healthwealth/", form)
        print(p)
        r = self.client.post("/integrations/add_healthwealth/remove_integration/1/", form)
        self.assertEqual(r.status_code, 302)
