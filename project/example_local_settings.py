import os
import sys

#Import settings from project.settings
settings = sys.modules['project.settings']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Set to True if you have installed RabbitMQ, and you plan on using
# AMQP. I highly recommend usage of AMQP. Read more in Github wiki.
SMS_AMQP_ENABLED = True

# Set according to https://pika.readthedocs.org/en/latest/examples/using_urlparameters.html
SMS_AMQP_URL = "amqp://guest:guest@localhost/sms"
SMS_AMQP_QUEUE = "messages"

# Celery broker URL. Can be the same as SMS_AMQL_URL
BROKER_URL = "amqp://guest:guest@localhost/sms"

# If True you must use passwords in phones
SMS_USE_AUTH = True

# Database settings
# If you are OK with using sqlite, leave default. For configuring mysql/postgresql consult
# Django documentation https://docs.djangoproject.com/en/1.8/ref/databases/
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db/sms.sqlite3'),
    },
}