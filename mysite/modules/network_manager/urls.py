from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^network_manager_list/$', views.network_manager_list, name='network_manager_list'),
    url(r'^add_network_manager/$', views.add_network_manager, name='add_network_manager'),
    url(r'^edit_network_manager/$', views.add_network_manager, name='edit_network_manager'),
    url(r'^del_network_manager/$', views.del_network_manager, name='del_network_manager'),
]
