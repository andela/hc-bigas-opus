from datetime import timedelta

from django.test import Client, TestCase

from hc.api.models import Check, Ping

from django.utils import timezone


class PingTestCase(TestCase):

    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert r.status_code == 200

        self.check.refresh_from_db()
        assert self.check.status == "up"

        ping = Ping.objects.latest("id")
        assert ping.scheme == "http"

    def test_it_handles_bad_uuid(self):
        r = self.client.get("/ping/not-uuid/")
        assert r.status_code == 400

    def test_it_handles_120_char_ua(self):
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/44.0.2403.89 Safari/537.36")

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        assert r.status_code == 200

        ping = Ping.objects.latest("id")
        assert ping.ua == ua

    def test_it_truncates_long_ua(self):
        ua = "01234567890" * 30

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        assert r.status_code == 200

        ping = Ping.objects.latest("id")
        assert len(ping.ua) == 200
        assert ua.startswith(ping.ua)

    def test_it_reads_forwarded_ip(self):
        ip = "1.1.1.1"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's remote address
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ping.remote_addr, ip)

        ip = "1.1.1.1, 2.2.2.2"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        assert r.status_code == 200
        assert ping.remote_addr == "1.1.1.1"

    def test_it_reads_forwarded_protocol(self):
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's scheme

    def test_it_never_caches(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert "no-cache" in r.get("Cache-Control")

    ### Test that when a ping is made a check with a paused status changes status
    def test_it_changes_status_of_check(self):
        self.check.status = 'paused'
        self.check.save()
        self.client.get("/ping/%s/" % self.check.code)
        self.check.refresh_from_db()
        self.assertEqual(self.check.status, "up")
    ### Test that a post to a ping works
    def test_post_to_ping_works(self):
        r = self.client.post("/ping/%s/" % self.check.code)
        self.assertEqual(r.status_code, 200)

    ### Test that the csrf_client head works
    def test_csrf_client_head_works(self):
        csrf_client = Client(enforce_csrf_checks=True)
        r = csrf_client.head("/ping/%s/" % self.check.code)

        self.assertEqual(r.status_code, 200)

    def test_it_handles_often(self):
        """Test it can note when a job runs too often"""
        self.check.status = "up"
        self.check.last_ping = timezone.now() - timedelta(minutes=1200)
        self.check.save()
        r = self.client.get("/ping/%s/" % self.check.code)
        self.check.refresh_from_db()
        self.assertTrue(self.check.often)
