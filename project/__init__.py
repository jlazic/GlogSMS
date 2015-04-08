from __future__ import absolute_import
from django.conf import settings

if settings.USE_CELERY:
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app