# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.contrib import admin
from sms.models import Message, Request, StatusLog, Phone
import reversion


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'recipient', 'user', 'sender', 'message', 'status', 'added')


class RequestAdmin(admin.ModelAdmin):
    model = Request
    list_display = ('id', 'phone_number', 'log', 'battery', 'network', 'send_limit', 'action', 'added')


class StatusLogAdmin(admin.ModelAdmin):
    model = Request
    list_display = ('id', 'message', 'phone_number', 'status', 'log', 'error', 'added')


class PhoneAdmin(reversion.VersionAdmin):
    model = Phone
    list_display = ('id', 'model', 'number', 'imei', 'serial', 'is_active', 'added')

admin.site.register(Message, MessageAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(StatusLog, StatusLogAdmin)
admin.site.register(Phone, PhoneAdmin)