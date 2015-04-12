# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.db.models.signals import post_save
from django.dispatch import receiver
from sms.models import Message
import pika
from django.conf import settings

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
            parameters = pika.URLParameters(settings.SMS_AMQP_URL)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(settings.SMS_AMQP_QUEUE)
            channel.basic_publish(exchange='', routing_key='messages', body=instance.to_json())
            connection.close()
        except Exception, e:
            print e
