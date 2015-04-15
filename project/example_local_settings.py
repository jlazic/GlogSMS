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

# Set to integer number (hours) if you want archive all sent messages older than X hours. I do not recommend to set this
# to value lower than 24.
# WARNING!!! This will remove message text to send messages older than X hours, and replace it with SHA hash.
# For more understanding read sms.models.archive function comment
SMS_ARCHIVE_MESSAGES = False

# Enter administrator email here. You can enter multiple addresses
# These users will receive email notifications and error reports
# https://docs.djangoproject.com/en/1.8/ref/settings/#admins
ADMINS = (('Administrator', 'administrator@example.com'))

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'glogsms@example.com'

# Database settings
# If you are OK with using sqlite, leave default. For configuring mysql/postgresql consult
# Django documentation https://docs.djangoproject.com/en/1.8/ref/databases/
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db/sms.sqlite3'),
    },
}