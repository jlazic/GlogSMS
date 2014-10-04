__author__ = 'josip.lazic'

from django.core.management.base import BaseCommand, CommandError
from sms.models import Message
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = ''
    help = 'Archive SMS messages older than 24 hours'

    def handle(self, *args, **options):
        how_many_hours = 24
        messages = Message.objects.filter(updated__lte=datetime.now()-timedelta(hours=how_many_hours))
        for message in messages:
            print "Archiving: "+str(message)
            message.archive()