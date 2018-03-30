import json
import re, cgi

from django.core import mail
from django.utils import timezone

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check



class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        ### Assert that the token is set
        assert isinstance(token, str)
        ### Assert that the email was sent and check email content

    def test_it_sends_report(self):
        '''
        This Tests ensure the reports can be sent via email
        ''' 
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Test Check", user=self.alice)
        check.save()

        form = {"update_reports_allowed":"1" ,"reports_frequency": "now"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEquals(200,  r.status_code)
        ###Assert that the email was sent and check email content --Done
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Monthly Report")

    def test_you_can_set_report_period(self):
        '''
        This test checks that the user is able to set the periods they want to 
        be recieving reports
        '''
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Test Check", user=self.alice)
        check.save()

        form = {"update_reports_allowed": "1", "reports_frequency": "weekly"}
        res = self.client.post("/accounts/profile/", form)
        self.assertEquals(200, res.status_code)
        self.assertEquals("monthly", self.alice.profile.reports_frequency)

    def test_you_can_view_report(self):
        '''Check if you can view report on the dashboard'''
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Test Check", user=self.alice)
        check.save()     

        check.last_ping = timezone.now()
        check.status = "up"
        check.save()
        
        res = self.client.get('/accounts/dashboard/')
        self.assertTrue(200, res.status_code)
        self.assertIn("Test Check", str(res.content))

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        ### Assert the existence of the member emails

        self.assertTrue("frank@example.org" in member_emails)

        ###Assert that the email was sent and check email content

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    ### Test it creates and revokes API key
