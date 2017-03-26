from django.conf.urls import url
from . import views
from .code import command, basic_data_monitor, illegal_website

urlpatterns = [
    # 指令
    url(r'^command_list/$', command.command_list, name='command_list'),
    url(r'^add_command/$', command.add_command, name='add_command'),
    url(r'^del_command/$', command.del_command, name='del_command'),

    # 基础数据监测
    url(r'^basic_data_monitor/$', basic_data_monitor.basic_data_monitor, name='basic_data_monitor'),

    # 违法违规网站监测
    url(r'^illegal_website_list/$', illegal_website.illegal_website_list, name='illegal_website_list'),
]

