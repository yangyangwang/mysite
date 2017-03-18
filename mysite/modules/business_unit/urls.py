from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^business_unit_list/$', views.business_unit_list, name='business_unit_list'),
	url(r'^add_business_unit/$', views.add_business_unit, name='add_business_unit'),
	url(r'^del_business_unit/$', views.del_business_unit, name='del_business_unit'),


	# url(r'^business_unit_list/$', views.BusinessUnitList.as_view(), name='business_unit_list'),
	# url(r'^add_business_unit/$', views.BusinessUnitCreate.as_view(), name='add_business_unit'),
]

