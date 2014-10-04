# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='password',
            field=models.CharField(default=1234, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='added',
            field=models.DateTimeField(help_text=b'Date and time when message was added to database. ie. 2010-11-10T03:07:43', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='is_archived',
            field=models.BooleanField(default=False, help_text=b'Archived messages have message field removed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(help_text=b'SMS message. Messages longer than 160 characters will be sent as multipart', max_length=1024, validators=[django.core.validators.MinLengthValidator(1)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.CharField(help_text=b'Recipient mobile number, ie. 0981234567', max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(help_text=b'Sender ie. Agronet, ISAP, PRTG,...', max_length=128, null=True, validators=[django.core.validators.MinLengthValidator(1)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='updated',
            field=models.DateTimeField(help_text=b'Date and time when message was last modified. ie. 2010-11-10T03:07:43', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='log',
            field=models.TextField(help_text=b'Mobile phone logs', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='phone_number',
            field=models.CharField(help_text=b'Mobile phone number that returned this status.', max_length=128),
            preserve_default=True,
        ),
    ]
