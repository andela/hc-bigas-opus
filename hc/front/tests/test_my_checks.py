from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/checks/")
            self.assertContains(r, "Alice Was Here", status_code=200)

    def test_it_shows_green_check(self):
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-up")

        # Mobile
        self.assertContains(r, "label-success")

    def test_it_shows_red_check(self):
        self.check.last_ping = timezone.now() - (td(days=1) + td(hours=1))
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-down")

        # Mobile
        self.assertContains(r, "label-danger")

    def test_it_shows_amber_check(self):
        self.check.last_ping = timezone.now() - td(days=1, minutes=30)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-grace")

        # Mobile
        self.assertContains(r, "label-warning")

    def test_it_shows_purple_check(self):
        self.check.last_ping = timezone.now() - td(minutes=1200)
        self.check.status = "up"
        self.check.save()
        self.client.get("/ping/%s/" % self.check.code)
        self.check.refresh_from_db()

    def test_it_shows_nag_check(self):
        self.client.login(username="alice@example.org", password="password")

        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "nag"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-bullhorn")

        # Mobile 
        self.assertContains(r,"label-nag")
