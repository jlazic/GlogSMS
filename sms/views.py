# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'

import json
from django.http import HttpResponse, HttpResponseNotAllowed
from sms.models import StatusLog, Phone, Message
from sms.forms import RequestForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from jsonview.decorators import json_view
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from forms import MessageForm
from django.conf import settings
from django.core.exceptions import PermissionDenied


class Redirect(RedirectView):
    url = '/sms/user/send/'


class Index(CreateView):
    template_name = 'sms/user_send_message.html'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Index, self).dispatch(*args, **kwargs)


class MessageDetail(DetailView):
    model = Message

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MessageDetail, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class MessageList(ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


@csrf_exempt
@json_view
def pool(request):
    """
    Implementation of EnvayaSMS API http://sms.envaya.org/serverapi/
    :param request:
    :return:
    """

    # We must allow HEAD verb in order for phones to being able to ping server
    if request.method == 'HEAD':
        return HttpResponse('OK')

    # Deny any other verb except POST
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST requests allowed here')

    """
    First, save incoming request to database via RequestForm. We save all incoming requests without discrimination
    based on wrong passwords, missing settings,... yeah, this could bite me in the ass later on.
    """
    rf = RequestForm(request.POST)
    r = rf.save()

    """
    After we have saved request to database, check if we have this phone in database
    If there is no such phone this will fail with error 403, and it will be written to log file
    """
    try:
        phone = Phone.objects.get(number=request.POST['phone_number'])
    except Phone.DoesNotExist:
        raise PermissionDenied('We have no phone with number {} configured'.format(request.POST['phone_number']))


    """
    If we use authentication check phones password against X-Request-Signature sent by phone
    """
    if settings.SMS_USE_AUTH:
        url = request.build_absolute_uri()
        request_signature = phone.calculate_signature(url, request.POST)
        if request_signature != request.META['HTTP_X_REQUEST_SIGNATURE']:
            raise PermissionDenied('You have an invalid password. What is your first dogs name?')

    events = None
    json_response = '{}'  # Default empty JSON response

    """Sada idemo lijepo redom po svim mogucim opcijama, pocevsi sa outgoing, send_status, incoming,..."""
    if request.POST['action'] == 'outgoing':
        """Additional parameters sent in POST requests with action=outgoing: (None)"""
        # Sending max 5 messages at once, poor mans throttling
        messages = Message.objects.filter(status='queued')[:5]  # status=queued, Server queue
        events = {'events': [{'event': 'send', 'messages': []}]}  # Inicijaliziramo prazane evente
        for message in messages:
            # Grozno izgleda kako python barata sa nestanim listama i dictovima, ali sta da se radi.
            events['events'][0]['messages'].append(
                {'id': message.id, 'to': message.phone_number(), 'message': message.message}
            )
            message.status = 'sent'
            message.save()

        json_response = json.dumps(events)


    # Server salje send_status za poruke koje imaju message.id
    elif request.POST['action'] == 'send_status':
        m = get_object_or_404(Message, pk=request.POST['id'])  # Pronajdi poruku, ili vrati 404 gresku
        s = StatusLog(status=request.POST['status'], error=request.POST['error'], log=request.POST['log'],
                      phone_number=request.POST['phone_number'], message=m)
        s.save()
        m.update_status(request.POST['status'])

    return HttpResponse(json_response, content_type='application/json')


"""
DRF API related views
"""
from sms.models import Message
from rest_framework import viewsets, mixins
from sms.serializers import MessageSerializer

class MessageAPIList(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Messages list, filtered by current user
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Filter only messages for currently authenticated user
        """
        user = self.request.user
        return Message.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


