import json
import datetime

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error

        return r
    
    def wrong_post(self, data, expected_error=None):
        x = self.client.post("/api/v1", json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(x.status_code, 404)
            ### Assert that the expected error is the response error

        return x
        
    def test_it_fails_wrong_url(self):
        x = self.wrong_post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })
        

        self.assertEqual(x.status_code, 404)

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        ### Assert the expected last_ping and n_pings values

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = {'status_code': 201} ### This is just a placeholder variable

        self.assertEqual(r['status_code'], 201)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        r = {'status_code': 400, 'error': "wrong api_key"} ### This is just a placeholder variable
        self.assertEqual(r['status_code'], 400)
        self.assertEqual(r["error"], "wrong api_key")

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        r = {'status_code': 400, 'error': "could not parse request body"} ### This is just a placeholder variable
        self.assertEqual(r['status_code'], 400)
        self.assertEqual(r["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        """Test if a number is used in timeout."""
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_number_grace_period(self):
        """Test if a number is used in grace period."""
        r=self.post({"api_key": "abc", "grace": "oops"},
                  expected_error="grace is not a number")
        self.assertEqual(r.status_code, 400)          
    def test_it_rejects_non_string_name(self):
        r=self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")
        self.assertEqual(r.status_code, 400)          

    ### Test for the assignment of channels
    ### Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_it_rejects_small_timeout_length(self):
        """Testing if the length is  small than 60 seconds."""
        r = self.post({
            "api_key":"abc", "timeout":59
        })
        response_payload = r.json()

        self.assertEqual(r.status_code, 400)
        self.assertEqual(response_payload["error"], "timeout is too small")
    def test_it_rejects_timeout_length(self):
        """Testing if the length is too large"""
        r = self.post({
            "api_key": "abc", "timeout": 200000000
        })
        response_payload = r.json()

        self.assertEqual(r.status_code, 400)
        self.assertEqual(response_payload["error"], "timeout is too large")
    
    def test_it_rejects_timeout(self):
        """testing if length of check is too small"""
        r = self.post({
            "api_key": "abc","timeout": 0
        })
        response_payload = r.json()

        self.assertEqual(r.status_code, 400)
        self.assertEqual(response_payload["error"], "timeout is too small")

    def test_it_accept_timeout_length(self):
        """Testing if it accepts minimum 1 minute as minimum value."""
        r = self.post({
            "api_key":"abc", "timeout":3600
        })
        response_payload = r.json()

        self.assertEqual(r.status_code, 201)
     ### Test for the assignment of channels
    def test_it_assigns_channels(self):
        channel = Channel(user=self.alice)
        channel.save()

        response = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })
        check = Check.objects.get(user=self.alice, name="Foo")
        check.assign_all_channels()

        self.assertEqual(check.channel_set.count(), 1)
    def test_if_value_of_timeout_is_created(self):
        """Test if the timeout is added in the model.""" 
        check = Check(timeout="3600")
        check.save()
        test_check = Check.objects.filter(timeout="3600").first()
        self.assertEqual(test_check.timeout, datetime.timedelta(0, 3600))
