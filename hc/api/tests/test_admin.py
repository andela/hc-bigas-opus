from hc.api.models import Channel, Check
from hc.test import BaseTestCase
from django.contrib.auth.models import User


class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

    # Set Alice to be staff and superuser and save her :)
    def test_if_alice_is_set_to_super_user_and_saved(self):
        # store the password to login later
        password = 'password'
        my_admin = User.objects.create_superuser('admin', 'alice@example.org', password)
        my_admin.save()
        my_admin.is_staff = True
        my_admin.save()
        self.assertTrue(my_admin.is_staff)
        self.assertTrue(my_admin.is_superuser)

    def test_it_shows_channel_list_with_pushbullet(self):
        self.client.login(username="alice@example.org", password="password")

        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()
        # Assert for the push bullet
        self.assertEqual("pushbullet", ch.kind)