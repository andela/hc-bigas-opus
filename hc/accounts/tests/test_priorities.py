from hc.test import BaseTestCase
from django.contrib.auth.models import User
from hc.accounts.models import Member
from hc.api.models import Check


class SetPriorities(BaseTestCase):

    def test_it_sets_default_priority(self):
        self.client.login(username="alice@example.org", password="password")
        self.client.login(username="frank@example.org")
        check = Check(name="Test Check", user=self.alice)
        check.save()

        form = {"invite_team_member": "1", "email": "frank@example.org", "check": "Test Check"}
        self.client.post("/accounts/profile/", form)

        user = User.objects.filter(email=form["email"]).first()
        member = Member.objects.filter(user=user).first()
        self.assertEqual(member.priority, "LOW")

    def test_it_changes_priority(self):
        self.client.login(username="alice@example.org", password="password")
        self.client.login(username="frank@example.org")
        check = Check(name="Test Check", user=self.alice)
        check.save()

        form = {"invite_team_member": "1", "email": "frank@example.org", "check": "Test Check"}
        self.client.post("/accounts/profile/", form)

        form = {"member_priority": "HIGH", "email": "frank@example.org", "check": "Test Check"}
        self.client.post("/accounts/profile/", form)

        user = User.objects.filter(email=form["email"]).first()
        member = Member.objects.filter(user=user).first()
        self.assertEqual(member.priority, "HIGH")
