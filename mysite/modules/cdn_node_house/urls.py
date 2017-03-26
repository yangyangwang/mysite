from django.conf.urls import url

from . import views
from .code import report_house_info

urlpatterns = [
    url(r'^cdn_node_house_list/$', views.cdn_node_house_list, name='cdn_node_house_list'),
    url(r'^add_cdn_node_house/$', views.add_cdn_node_house, name='add_cdn_node_house'),
    url(r'^del_cdn_node_house/$', views.del_cdn_node_house, name='del_cdn_node_house'),

    url(r'^house_link_list/$', views.house_link_list, name='house_link_list'),
    url(r'^add_house_link/$', views.add_house_link, name='add_house_link'),
    url(r'^del_house_link/$', views.del_house_link, name='del_house_link'),

    url(r'^house_frame_list/$', views.house_frame_list, name='house_frame_list'),
    url(r'^add_house_frame/$', views.add_house_frame, name='add_house_frame'),
    url(r'^del_house_frame/$', views.del_house_frame, name='del_house_frame'),

    url(r'^house_ipseg_list/$', views.house_ipseg_list, name='house_ipseg_list'),
    url(r'^add_house_ipseg/$', views.add_house_ipseg, name='add_house_ipseg'),
    url(r'^del_house_ipseg/$', views.del_house_ipseg, name='del_house_ipseg'),

    url(r'^report_house_info/$', report_house_info.report_house_info, name='report_house_info'),
    
]
