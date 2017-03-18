#coding=utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from .models import Userinfo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def index(request):
	return HttpResponse("Hello World!")


def user_list(request):
	user_list = Userinfo.objects.all()
	print("-------")
	print(user_list)
	print(locals())
	return render_to_response('table.html', locals())

# 取消csrftoken验证
@csrf_exempt
def add_user(request):
	print("@add_user")
	name = request.POST['name']
	address = request.POST['address']
	city = request.POST['city']
	Userinfo.objects.create(
		name = name,
		address = address,
 		city = city,
	)
	return HttpResponse("添加成功！")
