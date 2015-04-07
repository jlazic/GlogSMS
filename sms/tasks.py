__author__ = 'josip.lazic'

from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task()
def send_email(address):
    print address
    return address


@app.task
def add(x, y):
    send_email.delay('josip@lazic.info')
    return x + y