from hc.api.models import Check
from hc.test import BaseTestCase


class UpdateTimeoutTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateTimeoutTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 3600
        assert check.grace.total_seconds() == 60
        assert check.nag.total_seconds() == 3600

    def test_team_access_works(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 7200, "grace": 60, "nag": 3600}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, data=payload)

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 7200

    def test_it_handles_bad_uuid(self):
        url = "/checks/not-uuid/timeout/"
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        assert r.status_code == 400

    def test_it_handles_missing_uuid(self):
        # Valid UUID but there is no check for it:
        url = "/checks/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/timeout/"
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        assert r.status_code == 404

    def test_it_checks_ownership(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url, data=payload)
        assert r.status_code == 403
        
    def test_update_timeout_and_grace_works(self):
        """Test if grace and timeout updates."""
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 3600
        assert check.grace.total_seconds() == 60
        assert check.nag.total_seconds() == 3600
        # 
        payload = {"timeout": 300, "grace": 90,"nag": 3600}
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")
        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 300 
        assert check.grace.total_seconds() == 90 
            

def test_update_timeout_and_nag_works(self):
        """Test if nag,grace and timeout updates."""
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60, "nag": 3600}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 3600
        assert check.grace.total_seconds() == 60
        assert check.nag.total_seconds() == 3600
        # 
        payload = {"timeout": 300, "grace": 90,"nag": 300}
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")
        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 300 
        assert check.grace.total_seconds() == 90
        assert check.grace.total_seconds() == 300 
