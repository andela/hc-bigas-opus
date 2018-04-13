from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone
from django.contrib.auth.models import User
from hc.front.forms import (PriorityForm)



class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        bob = User.objects.get(email="bob@example.org")
        self.check = Check(user=self.alice, name="Alice was Here", membership_access=True, member_id = bob.id)
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/checks/")
            self.assertContains(r, "alice@example.org", status_code=200)

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

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "fa-history")

        # Mobile
        self.assertContains(r, "label-info")

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
    
    def test_it_sets_priority(self):
        self.client.login(username="alice@example.org", password="password")
        self.check.priority  = 2
        self.check.save()
        
        
        r = self.client.post("/checks/{}/priority/".format(self.check.code),{'priority_select':1})

        self.assertTrue(self.check.priority,1)
        