# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.CharField(help_text=b'Telefonski broj oblika 0981234567', max_length=128)),
                ('sender', models.CharField(help_text=b'Posiljatelj, npr. Agronet, ISAP, PRTG,...', max_length=128, null=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('message', models.TextField(help_text=b'SMS poruka, poruke iznad 160 znakova ce biti poslane kao multipart SMS', max_length=1024, validators=[django.core.validators.MinLengthValidator(1)])),
                ('status', models.CharField(default=b'queued', help_text=b'Status: queued, sent, delivered, failed, cancelled. Default: queued', max_length=b'32', choices=[(b'queued', b'Queued'), (b'sent', b'Sent to Phone'), (b'delivered', b'Delivered'), (b'failed', b'Failed'), (b'cancelled', b'Cancelled'), (b'archived', b'Archived')])),
                ('is_archived', models.BooleanField(default=False, help_text=b'Arhiviranim porukama je obrisano polje message')),
                ('added', models.DateTimeField(help_text=b'Datum i vrijeme kada je poruka dodana u bazu. Ex: 2010-11-10T03:07:43', auto_now_add=True)),
                ('updated', models.DateTimeField(help_text=b'Datum i vrijeme kada je poruka dodana u bazu. Ex: 2010-11-10T03:07:43', auto_now=True)),
                ('user', models.ForeignKey(help_text=b'User ID', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=128)),
                ('number', models.CharField(max_length=32)),
                ('imei', models.CharField(max_length=64)),
                ('serial', models.CharField(max_length=128)),
                ('PIN', models.CharField(max_length=64)),
                ('ip', models.IPAddressField()),
                ('is_active', models.BooleanField(default=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('phone_number', models.CharField(max_length=128)),
                ('log', models.TextField(null=True, blank=True)),
                ('network', models.CharField(max_length=32)),
                ('settings_version', models.IntegerField()),
                ('now', models.IntegerField()),
                ('battery', models.IntegerField()),
                ('power', models.IntegerField()),
                ('action', models.CharField(max_length=64, choices=[(b'incoming', b'Incomming'), (b'outgoing', b'Outgoing'), (b'send_status', b'Send status'), (b'device_status', b'Device status'), (b'test', b'Test'), (b'amqp_started', b'AMQP started'), (b'forward_sent', b'Forward sent')])),
                ('status', models.CharField(max_length=64, null=True, blank=True)),
                ('send_limit', models.IntegerField(null=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(help_text=b'Telefonski broj mobitela koji je vratio ovaj status log.', max_length=128)),
                ('status', models.CharField(help_text=b'Status', max_length=32, choices=[(b'queued', b'Queued'), (b'failed', b'Failed'), (b'cancelled', b'Cancelled'), (b'sent', b'Sent'), (b'requeueing', b'Requeueing')])),
                ('log', models.TextField(help_text=b'Tekstualni logovi sa mobitela', null=True, blank=True)),
                ('error', models.CharField(max_length=1024)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('message', models.ForeignKey(related_name='status_log', to='sms.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('is_active', 'ip')]),
        ),
    ]
