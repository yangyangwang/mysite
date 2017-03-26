from django.conf.urls import url
from .code import se_command, se_ip, se_domain

urlpatterns = [
    url(r'^suspected_exception_command_list/$', se_command.suspected_exception_command_list, 
        name='suspected_exception_command_list'),
    url(r'^suspected_exception_ip_list/$', se_ip.suspected_exception_ip_list, 
        name='suspected_exception_ip_list'),
    url(r'^suspected_exception_domain_list/$', se_domain.suspected_exception_domain_list, 
        name='suspected_exception_domain_list'),
]
