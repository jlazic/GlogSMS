import os
import sys

#Import settings from project.settings
settings = sys.modules['project.settings']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SMS_AMQP_ENABLED = True
SMS_AMQP_URL = "amqp://guest:guest@localhost/sms"

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db/sms.sqlite3'),
    },
}