import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check
from hc.accounts.models import Member

from hc.api.models import Channel

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(alert_after__gt=now, status="down")
        going_often = query.filter(alert_after__lt=now, status="often")
        nag_down = query.filter(nag_after__lt=now, status="down")
        nag_up = query.filter(nag_after__gt=now, status="nag")
        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + list(going_up.iterator()) + list(nag_down.iterator()) + list(nag_up.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check):
        """ Send an alert for a single check.
        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.
        """

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        if check.status == "down":

            self.notify_members(check)
            check.nag_after = timezone.now() + check.nag
            check.status = True
            check.nag_after = timezone.now() + check.nag
            check.status = "nag"
        
        elif check.status == "nag":
            check.nag_after = timezone.now() + check.nag 
            check.nag_after

        check.save()
        self.send_alert(check)
        connection.close()
        return True

    def send_alert(self, check):
        """
        This helper method  notifies a user
        """
        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert()
        if errors is not None:
            for ch, error in errors:
                self.stdout.write("ERROR: %s %s %s\n" %
                                (ch.kind, ch.value, error))
                                
        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)

    def notify_members(self, check):
        """
        This method notifies members in the team
        """
        members = Member.objects.filter(
            team=check.user.profile).all()
        for member in members:
            if member.priority == "LOW" or (member.priority == "HIGH" and not check.is_alerted):
                channel = Channel.objects.filter(
                    value=member.user.email).first()
                check.is_alerted = True
                check.save()
                error = channel.notify(check)
                if error not in ("", "no-op"):
                    print("%s, %s" % (channel, error))
