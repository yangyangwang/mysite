from django.conf.urls import url
from .code import report_customer_info, app_service, customer_info,\
        domain_info, report_app_service, report_domain_info
from . import views

urlpatterns = [
    url(r'^customer_info_list/$', customer_info.customer_info_list, name='customer_info_list'),
    url(r'^add_customer_info/$', customer_info.add_customer_info, name='add_customer_info'),
    url(r'^del_customer_info/$', customer_info.del_customer_info, name='del_customer_info'),
    url(r'^report_customer_info/$', report_customer_info.report_customer_info, name='report_customer_info'),
    url(r'^logout_customer_info/$', report_customer_info.logout_customer_info, name='logout_customer_info'),

    url(r'^app_service_list/$', app_service.app_service_list, name='app_service_list'),
    url(r'^add_app_service/$', app_service.add_app_service, name='add_app_service'),
    url(r'^del_app_service/$', app_service.del_app_service, name='del_app_service'),
    url(r'^report_app_service/$', report_app_service.report_app_service, name='report_app_service'),

    url(r'^domain_info_list/$', domain_info.domain_info_list, name='domain_info_list'),
    url(r'^add_domain_info/$', domain_info.add_domain_info, name='add_domain_info'),
    url(r'^del_domain_info/$', domain_info.del_domain_info, name='del_domain_info'),
    url(r'^report_domain_info/$', report_domain_info.report_domain_info, name='report_domain_info'),
    
]
