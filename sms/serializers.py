# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from rest_framework import serializers
from sms.models import Message


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Django REST Framework serializer for message model
    """
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'sender', 'message', 'status', 'direction', 'type', 'is_archived', 'added',
                  'updated')
        read_only_fields = ('type', 'direction', 'status', 'is_archived')  # Hide these field from POST requests