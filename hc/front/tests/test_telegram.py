import json

from django.test.utils import override_settings
from hc.api.models import Channel
from hc.api.transports import SMS
from hc.test import BaseTestCase
from mock import patch


class AddSMSTestCase(BaseTestCase):

    def test_it_shows_instructions(self):
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/integrations/add_telegram/")
        self.assertContains(r, "@hckaliiBot", status_code=200)

    def test_it_adds_telegram(self):
        url = "/integrations/add/"
        form = {"kind": "telegram", "value": "-8734723234"}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1
