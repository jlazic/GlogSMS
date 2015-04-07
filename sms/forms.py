# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.forms import ModelForm
from models import Message, Request


class MessageForm(ModelForm):
    class Meta:
        fields = ['recipient', 'message', 'user', 'sender']
        model = Message


class RequestForm(ModelForm):
    class Meta:
        model = Request
        exclude = ['added', 'updated']