from __future__ import absolute_import

import pika
from django.conf import settings
from celery import shared_task


@shared_task
def queue_message(message):
    """
    Connect to RabbitMQ and publish SMS message in JSON format to the queue.
    From there mobile phones will pickup and send them.
    :param message:
    :return:
    """
    print "Sending... {}".format(message)
    parameters = pika.URLParameters(settings.SMS_AMQP_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(settings.SMS_AMQP_QUEUE)
    channel.basic_publish(exchange='', routing_key='messages', body=message.to_json())
    connection.close()