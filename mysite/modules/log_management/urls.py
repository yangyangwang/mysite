from django.conf.urls import url

from . import views
from .code import access_log, filter_log, monitor_log

urlpatterns = [
    url(r'^access_log_list/$', access_log.access_log_list, name='access_log_list'),
    url(r'^filter_log_list/$', filter_log.filter_log_list, name='filter_log_list'),
    url(r'^monitor_log_list/$', monitor_log.monitor_log_list, name='monitor_log_list'),
]
