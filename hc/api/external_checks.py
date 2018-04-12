import requests
from hc.api.models import ExternalChecks
from django.shortcuts import render
from django.utils import timezone

def external_check():
    """Implements Alerts for third party services"""
    external_checks = ExternalChecks.objects.all()
    if external_check:
        for integration in external_checks:
            if integration:
                if timezone.now() == integration.base_time:
                    third_party = requests.get("%s" % integration.third_party_url)
                    if third_party.status_code == 200:
                         result = requests.get("%s" % integration.check_url)
    return external_checks
