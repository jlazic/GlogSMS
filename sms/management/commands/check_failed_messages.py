# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'


from django.core.management.base import BaseCommand, CommandError
from sms.models import Message, StatusLog
from datetime import datetime, timedelta
from django.core.mail import mail_admins
from django.conf import settings
from sms.tasks import queue_message

class Command(BaseCommand):
    """
    Command is called through Celery Beat scheduler every hour
    """
    args = ''
    help = 'Check for failed messages, and resend them'

    def handle(self, *args, **options):
        """
        Check for messages with status 'sent to phone' that were not updated in last hour, and try to resend these
        messages.
        TODO: Maybe have some limit on resending, after 3 resend actions, cancel message.
        """
        try:
            failed_messages = Message.objects.filter(status='sent', updated__lte=datetime.now() - timedelta(hours=1))
            for message in failed_messages:
                message.status = 'queued'
                s = StatusLog(status='requeueing', error='Poruka nije poslana unutar sat vremena',
                              log='Requeueing message due to inactivity in last hour',
                              phone_number='1234', message=message)
                s.save()
                message.save()
                if settings.SMS_AMQP_ENABLED:
                    # Send message to AMQP queue again. This could lead to one message being delivered multiple times.
                    # TODO: Test this!
                    queue_message.delay(message)
        except Exception, e:
            """
            Send email to ADMINS, but continue to process failed_messages
            """
            mail_admins('Error while checking for failed messages', str(e))
