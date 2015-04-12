__author__ = 'josip.lazic'

from celery import Celery
from django.conf import settings
import pika

app = Celery('tasks', broker=settings.SMS_CELERY_URL)

@app.task()
def queue_message(message):
    parameters = pika.URLParameters(settings.SMS_AMQP_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(settings.SMS_AMQP_QUEUE)
    channel.basic_publish(exchange='', routing_key='messages', body=message.to_json())
    connection.close()