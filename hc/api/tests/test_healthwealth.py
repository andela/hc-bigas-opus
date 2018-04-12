from hc.api.models import ExternalChecks
from hc.test import BaseTestCase


class HealthWealthTestCase(BaseTestCase):
    def setUp(self):
        super(HealthWealthTestCase, self).setUp()
        self.external_check = ExternalChecks()
        self.external_check.save()

    def test_it_takesuser_input(self):
        self.client.login(username="alice@example.org", password="password")
        data = {'third_party_url':'','check_url':'','name':'','ping_time_difference':''}
        r = self.client.post("/add_healthwealth/", data, content_type="application/json")
        pass

    def test_user_can_create_integration(self):
        url = "/add_healthwealth/"
        form = {'third_party_url':'','check_url':'','name':'','ping_time_difference':''}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        assertEqual(r.status_code, 200)

    def test_user_can_delete_integration(self):
        self.client.login(username="alice@example.org", password="password")
        pass
