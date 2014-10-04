# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.conf.urls import url, include
from rest_framework import routers
from sms import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageAPIList, base_name='Messages')


urlpatterns = [
    url(r'^user/send/$', views.Index.as_view(), name='index'),
    url(r'^user/message/(?P<pk>\d+)/$', views.MessageDetail.as_view(), name='message-detail'),
    url(r'^user/messages/$', views.MessageList.as_view(), name='message-list'),
    url(r'^pool$', views.pool, name='pool'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


