import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        ### Assert the response status code

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        ### Assert the expected length of checks
        self.assertEqual(len(checks), 2)
        ### Assert the checks Alice 1 and  #  Alice 2's timeout, grace, ping_url, status,
        ### Assert the checks Alice 1

        Alice_1 = checks["Alice 1"]
        check_1= dict(
            timeout=Alice_1["timeout"],
            grace=Alice_1["grace"],
            status=Alice_1["status"],
            last_ping=Alice_1["last_ping"],
            n_pings=Alice_1["n_pings"],
            ping_url=Alice_1["ping_url"]
        )
        expected_results = dict(
            timeout=3600,
            grace=900,
            status="new",
            last_ping=self.a1.last_ping.isoformat(),
            n_pings=1,
            ping_url=str(self.a1.url()),
        )
        self.assertEqual(check_1, expected_results)

        #  Alice 2's timeout, grace, ping_url, status,
        Alice_2 = checks["Alice 2"]
        check_2= dict(
            timeout=Alice_2["timeout"],
            grace=Alice_2["grace"],
            status=Alice_2["status"],
            last_ping=Alice_2["last_ping"],
            ping_url=Alice_2["ping_url"]
        )
        expected_results = dict(
            timeout= 86400,
            grace=3600,
            status="up",
            last_ping=self.a2.last_ping.isoformat(),
            ping_url=str(self.a2.url()),
        )
        self.assertEqual(check_2, expected_results)
        ### last_ping, n_pings and pause_url

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    ### Test that it accepts an api_key in the request
    def test_it_accepts_api_key_in_request(self):
        payload = json.dumps({"api_key": "abc"})
        r = self.client.generic(
            'GET', self.URL,
            payload,
            content_type="application/json"
        )

        self.assertEqual(r.status_code, 200)
