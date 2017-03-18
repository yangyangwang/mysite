from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cdn_net_list/$', views.cdn_net_list, name='cdn_net_list'),
    url(r'^add_cdn_net/$', views.add_cdn_net, name='add_cdn_net'),
    url(r'^del_cdn_net/$', views.del_cdn_net, name='del_cdn_net'),
]
