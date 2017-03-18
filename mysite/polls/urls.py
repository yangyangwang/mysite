from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^user_list/$', views.user_list, name='user_list'),
	url(r'^add_user/$', views.add_user, name='add_user'),
	url(r'^$', views.index, name='index'),
]
