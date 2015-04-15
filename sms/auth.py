# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.contrib.auth.middleware import RemoteUserMiddleware


class ApacheHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_PROXY_REMOTE_USER'