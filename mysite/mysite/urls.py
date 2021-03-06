"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('polls.urls')),
    url(r'', include('account.urls')),
    url(r'', include('modules.business_unit.urls')),
    url(r'', include('modules.network_manager.urls')),
    url(r'', include('modules.customer_info.urls')),
    url(r'', include('modules.cdn_net_info.urls')),
    url(r'', include('modules.cdn_node_info.urls')),
    url(r'', include('modules.cdn_node_house.urls')),
    url(r'', include('modules.active_resources.urls')),
    url(r'', include('modules.log_management.urls')),
    url(r'', include('modules.command_management.urls')),
    url(r'', include('modules.suspected_exception.urls')),

    url(r'^admin/', admin.site.urls),
]
