from django.conf.urls import url
from .code import cdn_net, mount_domain, mount_node

from . import views

urlpatterns = [
    # cdn子网列表，添加，编辑，删除
    url(r'^cdn_net_list/$', cdn_net.cdn_net_list, name='cdn_net_list'),
    url(r'^add_cdn_net/$', cdn_net.add_cdn_net, name='add_cdn_net'),
    url(r'^del_cdn_net/$', cdn_net.del_cdn_net, name='del_cdn_net'),

    # 上报cdn子网信息
    url(r'^report_cdn_net/$', cdn_net.report_cdn_net, name='report_cdn_net'),

    # 注销cdn子网信息
    url(r'^logout_cdn_net/$', cdn_net.logout_cdn_net, name='logout_cdn_net'),

    # 子网挂载cdn节点
    url(r'^mount_cdn_node/$', mount_node.mount_cdn_node, name='mount_cdn_node'),
    url(r'^save_mount_cdn_node/$', mount_node.save_mount_cdn_node, name='save_mount_cdn_node'),

    # 子网挂载加速域名
    url(r'^mount_cdn_domain/$', mount_domain.mount_cdn_domain, name='mount_cdn_domain'),
    url(r'^save_mount_cdn_domain/$', mount_domain.save_mount_cdn_domain, name='save_mount_cdn_domain'),
]
