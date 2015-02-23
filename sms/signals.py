# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.db.models.signals import post_save
from django.dispatch import receiver
from sms.models import Message
import pika
from django.conf import settings

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, **kwargs):
    print(instance.to_json())
    try:
        parameters = pika.URLParameters(settings.SMS_AMQP_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='messages')
        channel.basic_publish(exchange='', routing_key='messages', body=instance.to_json())
        connection.close()
    except Exception, e:
        print e
