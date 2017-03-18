from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cdn_node_list/$', views.cdn_node_list, name='cdn_node_list'),
    url(r'^add_cdn_node/$', views.add_cdn_node, name='add_cdn_node'),
    url(r'^del_cdn_node/$', views.del_cdn_node, name='del_cdn_node'),
]
