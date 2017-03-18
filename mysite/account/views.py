#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login(request):
	print ("@login")
	if request.method == "POST": #验证登录权限，进行登录
		print("post")
		home_page = "userinfo.html"
		#return HttpResponseRedirect(home_page)
		render_to_response(home_page)
	#return render_to_response('login.html')
	return render_to_response('userinfo.html')

def logout(request):
	pass
