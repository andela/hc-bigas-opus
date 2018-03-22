from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):

    def test_it_handles_missing_profile(self):
        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        self.client.login(username="ned@example.org", password="password")
        r = self.client.get("/about/")
        self.assertEqual(r.status_code, 200)

        ### Assert the new Profile objects count
    def test_profile_count(self):
        user = User(username="ned", email="ned@example.org")
        user.save()
        self.profile = Profile(user=user,  api_key="abc")
        self.profile.save()
        assert Profile.objects.count() == 1
