__author__ = 'josip@lazic.info'


from django.core.management.base import BaseCommand, CommandError
from sms.models import Message, StatusLog
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = ''
    help = 'Archive SMS messages older than 24 hours'

    def handle(self, *args, **options):
        """
        Hajmo vidjeti jel ima kakvih poruka koje su u stanju 'sent to phone', a da nisu updateane
        u zadnjih sat vremena. Bi bile poruke koje telefon mozda nikada nije ni preuzeo, jer za njih ni ne salje
        da su failale ili da su poslane. Uglavnom, takve poruke cemo slati ponovno
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
        except Exception, err:
            """
            Ako ulovis neki Exception, posalji poruku adminu da nesto nije OK
            Ovo se nikada ne bi smjelo desiti
            """
            alert_mesage = Message()
            alert_mesage.message = "Nesto nije OK sa slanjem SMS poruka: %s" % str(err)
            alert_mesage.sender = 'Localhost'
            alert_mesage.recipient = '0992492990'  # TODO: Stavio sam ovdje svoj mobitel, trebalo bi ovdje staviti neku varijablu
            alert_mesage.user = User.objects.get(pk=1)  # Postavi defaultno admin usera sa pk=1
            alert_mesage.save()