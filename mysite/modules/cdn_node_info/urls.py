from django.conf.urls import url
from .code import cdn_node, report_cdn_node

from . import views

urlpatterns = [
    url(r'^cdn_node_list/$', views.cdn_node_list, name='cdn_node_list'),
    url(r'^add_cdn_node/$', views.add_cdn_node, name='add_cdn_node'),
    url(r'^del_cdn_node/$', views.del_cdn_node, name='del_cdn_node'),

    url(r'^mount_cdn_house/$', cdn_node.mount_cdn_house, name='mount_cdn_house'),
    url(r'^save_mount_cdn_house/$', cdn_node.save_mount_cdn_house, name='save_mount_cdn_house'),

    url(r'^report_cdn_node/$', report_cdn_node.report_cdn_node, name='report_cdn_node'),
]
