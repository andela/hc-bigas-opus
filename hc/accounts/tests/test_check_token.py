from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_it_redirects_loggedin_users(self):
        form = {
            'email': self.alice.email,
            'password': 'password'
        }

        self.client.post(reverse('hc-login'), form, follow_redirects=True)
        response = self.client.post(reverse('hc-login'), form)
        self.assertRedirects(response, reverse('hc-checks'))

    ### Login with a bad token and check that it redirects
    def test_login_with_bad_token(self):
        url = reverse('hc-check-token', args=['bob', 'bad-token'])
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('hc-login'))

    ### Any other tests?
    ### Test if login link is sent after registration
    def test_login_link_is_sent(self):
        form = {
            'email': "chrisevans@marvel.com",
        }
        self.client.post(reverse('hc-login'), form)
        response = self.client.post(reverse('hc-login'), form)
        e = self.assertRedirects(response, reverse('hc-login-link-sent'))
