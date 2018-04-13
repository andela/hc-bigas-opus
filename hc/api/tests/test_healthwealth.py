from hc.api.models import ExternalChecks
from hc.test import BaseTestCase


class HealthWealthTestCase(BaseTestCase):
    def setUp(self):
        super(HealthWealthTestCase, self).setUp()
        self.external_check = ExternalChecks()
        self.external_check.save()

    def test_it_takesuser_input(self):
        self.client.login(username="alice@example.org", password="password")
        form = {'third_party_url':'','check_url':'','name':''}
        r = self.client.post("/add_healthwealth/", form)
        self.assertEqual(r.status_code, 200)

    def test_user_can_create_integration(self):
        url = "/add_healthwealth/"
        form = {'third_party_url':'','check_url':'','name':''}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        self.assertEqual(r.status_code, 200)

    def test_user_can_delete_integration(self):
        self.client.login(username="alice@example.org", password="password")
        # self.assertEqual(r.status_code, 302)
        pass
