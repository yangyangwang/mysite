from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..share_part.share_func import *
from .models import CdnNodeInfo
from ..dict_table.models import ReportStatus
import traceback
import json

# Create your views here.

def cdn_node_list(request):
	ret_list = CdnNodeInfo.objects.all()
	if ret_list:
		for one in ret_list:
			one.report_status = get_dict_name(one.report_status, ReportStatus)
	return render_to_response("cdn_node_info_list.html", locals())


def add_cdn_node(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}
	
	def _get():
		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = CdnNodeInfo.objects.get(id = tmp_id)
			
		return render_to_response('cdn_node_info_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")
        
	tmp_id = request.POST.get('id')
	cdn_node_id = request.POST.get('cdn_node_id')
	cdn_node_name = request.POST.get('cdn_node_name')

	def _update():
		try:
			CdnNodeInfo.objects.filter(id=tmp_id).update(
		        cdn_node_name = cdn_node_name
		    )
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		return HttpResponseRedirect('/cdn_node_list') 

	def _add():
	    try:
	        CdnNodeInfo.objects.create(
	            cdn_node_id = get_auto_16_id(),
	            cdn_node_name = cdn_node_name,
	            report_status = "1"
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))
	    return HttpResponseRedirect('/cdn_node_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


def del_cdn_node(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}

	tmp_id = request.POST.get('id')

	# 后续添加的业务逻辑
	# 如果节点信息要删除，也要将节点下挂载的都进行删除

	try:
	    CdnNodeInfo.objects.filter(id=tmp_id).delete()
	except:
	    return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))