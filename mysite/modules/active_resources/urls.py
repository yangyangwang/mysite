from django.conf.urls import url

from . import views
from .code import active_domain_info, active_ip_info

urlpatterns = [
    # 活跃域名
    url(r'^active_domain_info/$', active_domain_info.active_domain_info, name='active_domain_info'),
    url(r'^block_domain_info/$', active_domain_info.block_domain_info, name='block_domain_info'),

    # 活跃IP
    url(r'^active_ip_info/$', active_ip_info.active_ip_info, name='active_ip_info'),
    url(r'^block_ip_info/$', active_ip_info.block_ip_info, name='block_ip_info'),
]
