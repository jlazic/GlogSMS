# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.db.models.signals import post_save
from django.dispatch import receiver
from sms.models import Message
from django.conf import settings
from sms.tasks import queue_message

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    """
    Attach to Message post_save signal, and send message to RabbitMQ. Function will catch all exceptions and
    continue. This is as must because we don't want missing RabbitMQ to break SMS sending
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and settings.SMS_AMQP_ENABLED:
        print "Sending AMQP message"
        try:
            queue_message(instance).delay()
        except Exception, e:
            print e