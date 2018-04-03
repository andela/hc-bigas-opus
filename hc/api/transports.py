from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
import json
import os
import requests

from datetime import datetime
from twilio.rest import Client
from six.moves.urllib.parse import quote

from hc.lib import emails
import telegram

telegram_api = telegram.Bot(token=settings.TELEGRAM_TOKEN)

def tmpl(template_name, **ctx):
    template_path = "integrations/%s" % template_name
    return render_to_string(template_path, ctx).strip()


def custom_message(check):
    message = 'The Check ' + check.name + ' - ' + str(check.code)
    if check.status == 'down':
        message = "{} is DOWN \nLast ping {}".format(message,
        str(check.last_ping.strftime("%Y-%m-%d %H:%M:%S")))

        # message = message + ' is DOWN \nLast ping ' \
        # + str(check.last_ping.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        message = message + ' recieved a ping, UP now'
    return message

class Transport(object):
    def __init__(self, channel):
        self.channel = channel

    def notify(self, check, api=None):
        """ Send notification about current status of the check.

        This method returns None on success, and error message
        on error.

        """

        raise NotImplementedError()

    def test(self):
        """ Send test message.

        This method returns None on success, and error message
        on error.

        """

        raise NotImplementedError()

    def checks(self):
        return self.channel.user.check_set.order_by("created")


class Email(Transport):
    def notify(self, check, api=None):
        if not self.channel.email_verified:
            return "Email not verified"

        show_upgrade_note = False
        if settings.USE_PAYMENTS and check.status == "up":
            if not check.user.profile.team_access_allowed:
                show_upgrade_note = True

        ctx = {
            "check": check,
            "checks": self.checks(),
            "now": timezone.now(),
            "show_upgrade_note": show_upgrade_note
        }
        emails.alert(self.channel.value, ctx)


class HttpTransport(Transport):

    def request(self, method, url, **kwargs):
        try:
            options = dict(kwargs)
            if "headers" not in options:
                options["headers"] = {}

            options["timeout"] = 5
            options["headers"]["User-Agent"] = "healthchecks.io"

            r = requests.request(method, url, **options)
            if r.status_code not in (200, 201, 204):
                return "Received status code %d" % r.status_code
        except requests.exceptions.Timeout:
            # Well, we tried
            return "Connection timed out"
        except requests.exceptions.ConnectionError:
            return "Connection failed"

    def get(self, url):
        return self.request("get", url)

    def post(self, url, json, **kwargs):
        return self.request("post", url, json=json, **kwargs)

    def post_form(self, url, data):
        return self.request("post", url, data=data)


class Webhook(HttpTransport):
    def notify(self, check, api=None):
        url = self.channel.value_down
        if check.status == "up":
            url = self.channel.value_up

        if not url:
            # If the URL is empty then we do nothing
            return "no-op"

        # Replace variables with actual values.
        # There should be no bad translations if users use $ symbol in
        # check's name or tags, because $ gets urlencoded to %24

        if "$CODE" in url:
            url = url.replace("$CODE", str(check.code))

        if "$STATUS" in url:
            url = url.replace("$STATUS", check.status)

        if "$NAME" in url:
            url = url.replace("$NAME", quote(check.name))

        if "$TAG" in url:
            for i, tag in enumerate(check.tags_list()):
                placeholder = "$TAG%d" % (i + 1)
                url = url.replace(placeholder, quote(tag))

        return self.get(url)

    def test(self):
        return self.get(self.channel.value)


class Slack(HttpTransport):
    def notify(self, check, api=None):
        text = tmpl("slack_message.json", check=check)
        payload = json.loads(text)
        return self.post(self.channel.slack_webhook_url, payload)


class HipChat(HttpTransport):
    def notify(self, check, api=None):
        text = tmpl("hipchat_message.html", check=check)
        payload = {
            "message": text,
            "color": "green" if check.status == "up" else "red",
        }
        return self.post(self.channel.value, payload)


class PagerDuty(HttpTransport):
    URL = "https://events.pagerduty.com/generic/2010-04-15/create_event.json"

    def notify(self, check, api=None):
        description = tmpl("pd_description.html", check=check)
        payload = {
            "service_key": self.channel.value,
            "incident_key": str(check.code),
            "event_type": "trigger" if check.status == "down" else "resolve",
            "description": description,
            "client": "healthchecks.io",
            "client_url": settings.SITE_ROOT
        }

        return self.post(self.URL, payload)


class Pushbullet(HttpTransport):
    def notify(self, check, api=None):
        text = tmpl("pushbullet_message.html", check=check)
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {
            "Access-Token": self.channel.value,
            "Conent-Type": "application/json"
        }
        payload = {
            "type": "note",
            "title": "healthchecks.io",
            "body": text
        }

        return self.post(url, payload, headers=headers)


class Pushover(HttpTransport):
    URL = "https://api.pushover.net/1/messages.json"

    def notify(self, check, api=None):
        others = self.checks().filter(status="down").exclude(code=check.code)
        ctx = {
            "check": check,
            "down_checks": others,
        }
        text = tmpl("pushover_message.html", **ctx)
        title = tmpl("pushover_title.html", **ctx)
        user_key, prio = self.channel.value.split("|")
        payload = {
            "token": settings.PUSHOVER_API_TOKEN,
            "user": user_key,
            "message": text,
            "title": title,
            "html": 1,
            "priority": int(prio),
        }

        # Emergency notification
        if prio == "2":
            payload["retry"] = settings.PUSHOVER_EMERGENCY_RETRY_DELAY
            payload["expire"] = settings.PUSHOVER_EMERGENCY_EXPIRATION

        return self.post_form(self.URL, payload)


class VictorOps(HttpTransport):
    def notify(self, check, api=None):
        description = tmpl("victorops_description.html", check=check)
        payload = {
            "entity_id": str(check.code),
            "message_type": "CRITICAL" if check.status == "down" else "RECOVERY",
            "entity_display_name": check.name_then_code(),
            "state_message": description,
            "monitoring_tool": "healthchecks.io",
        }

        return self.post(self.channel.value, payload)

class SMS(HttpTransport):
    def notify(self, check, api=None):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=self.channel.value,
            from_=os.getenv('TWILIO_NUMBER'),
            body="Healthcheck update\n the Check {} is\n{}. \nLast ping: {}".format(
                check.name, check.status, check.last_ping.strftime('%x, %X'))
        )

class Telegram(HttpTransport):
    api = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    def notify(self, check, api=api):
        if api is None: api = Telegram.api
        send = api.send_message(
            chat_id=self.channel.value, text=custom_message(check))

class Shopify(HttpTransport):
    pass
