from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^customer_info_list/$', views.customer_info_list, name='customer_info_list'),
    url(r'^add_customer_info/$', views.add_customer_info, name='add_customer_info'),
    url(r'^del_customer_info/$', views.del_customer_info, name='del_customer_info'),

    url(r'^app_service_list/$', views.app_service_list, name='app_service_list'),
    url(r'^add_app_service/$', views.add_app_service, name='add_app_service'),
    url(r'^del_app_service/$', views.del_app_service, name='del_app_service'),

    url(r'^domain_info_list/$', views.domain_info_list, name='domain_info_list'),
    url(r'^add_domain_info/$', views.add_domain_info, name='add_domain_info'),
    url(r'^del_domain_info/$', views.del_domain_info, name='del_domain_info'),
    
]
