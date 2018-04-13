import requests
from hc.api.models import ExternalChecks
from django.shortcuts import render
from django.utils import timezone

def external_check():
    """Implements Alerts for third party services"""
    external_checks = ExternalChecks.objects.all()
    if external_checks:
        return external_checks
