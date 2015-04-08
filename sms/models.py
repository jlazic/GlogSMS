# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

from django.db import models
from django.contrib.auth.models import User
from hashlib import sha1
from django.core.validators import MinLengthValidator
import re
import json
from django.core.urlresolvers import reverse
from sms.helpers import ksort
import hashlib, base64


class Message(models.Model):
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('sent', 'Sent to Phone'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('archived', 'Archived'),
        ('incoming', 'Incoming')
    )

    DIRECTION_CHOICES = (
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing')
    )

    TYPE_CHOICES = (
        ('sms', 'SMS'),
        ('mms', 'MMS'),
        ('call', 'Call')
    )

    recipient = models.CharField(max_length=128, null=False, blank=False,
                                 help_text='Recipient mobile number, ie. 0981234567')
    user = models.ForeignKey(User, help_text='User ID')
    sender = models.CharField(max_length=128, validators=[MinLengthValidator(1)],
                              null=True, help_text='Sender ie. Agronet, ISAP, PRTG,...')
    message = models.TextField(max_length=1024, null=False, blank=False, validators=[MinLengthValidator(1)],
                               help_text='SMS message. Messages longer than 160 characters will be sent as multipart')
    status = models.CharField(choices=STATUS_CHOICES, default='queued', max_length='32',
                              help_text='Status: queued, sent, delivered, failed, cancelled. Default: queued')
    direction = models.CharField(choices=DIRECTION_CHOICES, default='outgoing', max_length='16',
                                 help_text='Message direction, incoming or outgoing')
    type = models.CharField(choices=TYPE_CHOICES, default='sms', max_length='8',
                            help_text='Mesage type, sms, mms or call')
    is_archived = models.BooleanField(default=False, help_text='Archived messages have message field removed')
    added = models.DateTimeField(auto_now_add=True,
                                 help_text='Date and time when message was added to database. ie. 2010-11-10T03:07:43')
    updated = models.DateTimeField(auto_now=True,
                                   help_text='Date and time when message was last modified. ie. 2010-11-10T03:07:43')

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return u'%s %s %s %s' % (self.id, self.sender, self.recipient, self.status)

    def get_absolute_url(self):
            return reverse('message-detail', kwargs={'pk': self.id})

    def update_status(self, status):
        """
        Update message status
        :param status:
        :return:
        """
        if status == "queued":
            pass
        elif status == "failed":
            self.status = 'failed'
            self.save()
        elif status == "cancelled":
            self.status = 'cancelled'
            self.save()
        elif status == "sent":
            self.status = 'delivered'
            self.save()
        return self

    def to_json(self):
        event = {'event': 'send', 'messages': [{'id': self.id, 'to': self.phone_number(), 'message': self.message}]}
        return json.dumps(event)

    def phone_number(self):
        """
        Function takes message number and removes all non-numeric characters
        ie. 099/2492 - 990 -> 0992492990
        We will not save this cleaned number in database, we use this function every time messages is sent to phone
        :return:
        """
        return re.sub("[^0-9]", "", self.recipient)

    def archive(self):
        """
        Hash message content to keep users privacy. We cannot hash/encrypt messages that have not been sent yet, for
        obvious reasons.
        Fist check if message status is Sent to Phone
        Change status to Archived. All delivered messages not changed in last 24 hours should be archived.
        This function is called through django management command
        :return:
        """
        if self.status == 'delivered' and not self.is_archived:
            self.message = sha1(self.message.encode('utf-8')).hexdigest()
            self.is_archived = True
            self.save()
        else:
            return False


class StatusLog(models.Model):
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('sent', 'Sent'),
        ('requeueing', 'Requeueing')
    )
    message = models.ForeignKey(Message, related_name='status_log')
    phone_number = models.CharField(max_length=128, help_text='Mobile phone number that returned this status.')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES,
                              help_text='Status')
    log = models.TextField(null=True, blank=True, help_text='Mobile phone logs')
    error = models.CharField(max_length=1024)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id) + " : " + str(self.status) + " : " + str(self.error)


class Request(models.Model):
    ACTION_CHOICES = (
        ('incoming', 'Incomming'),
        ('outgoing', 'Outgoing'),
        ('send_status', 'Send status'),
        ('device_status', 'Device status'),
        ('test', 'Test'),
        ('amqp_started', 'AMQP started'),
        ('forward_sent', 'Forward sent'),
    )

    version = models.IntegerField()
    phone_number = models.CharField(max_length=128)
    log = models.TextField(null=True, blank=True)
    network = models.CharField(max_length=32)
    settings_version = models.IntegerField()
    now = models.IntegerField()
    battery = models.IntegerField()
    power = models.IntegerField()
    action = models.CharField(max_length=64, choices=ACTION_CHOICES, null=False)
    status = models.CharField(max_length=64, blank=True, null=True)
    send_limit = models.IntegerField(null=True)
    added = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return str(self.id) + " " + self.action + " " + self.phone_number


class Phone(models.Model):
    """
    Model za sve telefone
    """
    model = models.CharField(max_length=128)
    number = models.CharField(max_length=32)
    imei = models.CharField(max_length=64)
    serial = models.CharField(max_length=128)
    PIN = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    ip = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.model

    class Meta:
        unique_together = ("is_active", "ip")

    def calculate_signature(self, url, post_data):
        """
        Calculate request signature
        X-Request-Signature
        A signature of the request to verify the phone and the server share the same password.
        The signature is calculated by the following algorithm:
        Sort all POST parameters, not including file uploads, by the name of the field (in the usual ASCII order).
        Generate an input string by concatenating:
        the server URL,
        each of the sorted POST parameters, in the format name=value for each name/value pair,
        the password,
        with a comma in between each element, like so:
        "<serverURL>,<name1>=<value1>,<...>,<nameN>=<valueN>,<password>"
        Generate the SHA-1 hash of the input string in UTF-8
        Encode the SHA-1 hash using Base64 with no line breaks.
        :param url:
        :param post_data:
        :param password:
        :return: string
        """

        request_signature = url
        for k,v in ksort(post_data):
            request_signature = '{},{}={}'.format(request_signature,k,v)
        request_signature = '{},{}'.format(request_signature, self.password)
        return base64.b64encode(hashlib.sha1(request_signature).digest())