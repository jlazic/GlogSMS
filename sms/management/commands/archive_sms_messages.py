# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.core.management.base import BaseCommand, CommandError
from sms.models import Message
from datetime import datetime, timedelta
from django.conf import settings


class Command(BaseCommand):
    """
    This command archives SMS messages that are delivered more that 24 hours ago. Command is executed via Celery Beat,
    you can enable/disable this setting in local_settings.py in SMS_ARCHIVE_MESSAGES
    """
    args = ''
    help = 'Archive SMS messages older than 24 hours'

    def handle(self, *args, **options):
        how_many_hours = settings.SMS_ARCHIVE_MESSAGES
        messages = Message.objects.filter(updated__lte=datetime.now()-timedelta(hours=how_many_hours))
        for message in messages:
            print "Archiving: "+str(message)
            message.archive()