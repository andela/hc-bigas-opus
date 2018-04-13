import requests
from hc.api.models import ExternalChecks
from django.shortcuts import render

def external_check():
    """Implements Alerts for third party services"""
    external_checks = ExternalChecks.objects.all()
    custom_integrations = []
    checks = []
    if external_check:
        for integration in external_checks:
            custom_integrations.append(integration.third_party_url)
            checks.append(integration.check_url)
        if len(custom_integrations) > 0:
            third_party = requests.get("%s" % custom_integrations[0])
            if third_party.status_code == 200:
                 result = requests.get("%s" % checks[0])
    return external_checks
