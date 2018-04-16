from django.test.utils import override_settings
from django.contrib.auth.models import User
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover",
                 "hipchat", "victorops","sms")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Settings", status_code=200)

    def test_bad_kinds_dont_work(self):
        """Test that bad kinds don't work"""
        url = "/integrations/add/"
        form = {"kind": "bad_kind", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        self.assertEquals(response.status_code, 400)

    ### Test that the team access works
    def test_team_access_works(self):
        """ test a team access"""
        alice_channel = User.objects.get(email="alice@example.org")
        alice_before = Channel.objects.filter(user=alice_channel).count()
        self.client.login(username="bob@example.org", password="password")
        url = "/integrations/add/"
        form = {"kind": "hipchat"}
        self.client.post(url, form)
        alice_after = Channel.objects.filter(user=alice_channel).count()
        self.assertEqual(alice_after, (alice_before + 1))

    def test_sms_access_works(self):
        """ test sms access"""
        alice_channel = User.objects.get(email="alice@example.org")
        alice_before = Channel.objects.filter(user=alice_channel).count()
        self.client.login(username="bob@example.org", password="password")
        url = "/integrations/add/"
        form = {"kind": "sms"}
        self.client.post(url, form)
        alice_after = Channel.objects.filter(user=alice_channel).count()
        self.assertEqual(alice_after, (alice_before + 1))
