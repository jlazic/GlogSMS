from django.conf.urls import patterns, include, url

from django.contrib import admin
from sms.views import Redirect
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Redirect.as_view(), name='redirect_to_sms'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sms/', include('sms.urls')),
)