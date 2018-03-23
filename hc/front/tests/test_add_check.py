""""
This Test ensures a user can be able to add check(cron jobs)
"""
from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    """ Test if checks can be added"""

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_work_access(self):
        '''Checks that people of the same team can see each others checks'''
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url)
        self.client.logout()

        # login another user 
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        assert Check.objects.count() == 2

    def test_login_required(self):
        ''' Checks that user need to logIn to add'''
        url = "/checks/add/"
        r = self.client.post(url)
        assert r.status_code == 302
        




    
