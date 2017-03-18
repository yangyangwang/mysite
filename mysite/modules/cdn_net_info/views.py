from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..share_part.share_func import *
from ..dict_table.models import ReportStatus
from .models import CdnNetInfo
import traceback
import json

# Create your views here.

def cdn_net_list(request):
	ret_list = CdnNetInfo.objects.all()
	if ret_list:
		for one in ret_list:
			one.report_status = get_dict_name(one.report_status, ReportStatus)
	return render_to_response("cdn_net_info_list.html", locals())


def add_cdn_net(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}
	
	def _get():
		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = CdnNetInfo.objects.get(id = tmp_id)
			
		return render_to_response('cdn_net_info_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")
        
	tmp_id = request.POST.get('id')
	cdn_net_id = request.POST.get('cdn_net_id')
	cdn_top_domain = request.POST.get('cdn_top_domain')
	top_domain_record_num = request.POST.get('top_domain_record_num')


	def _update():
		try:
			# 如果上报状态为新增已上报，更新未上报，更新已上报修改时都变为更新未上报
			# 如果为新增未上报，不用修改
			report_status = get_report_status(tmp_id, CdnNetInfo)
			if report_status in ["2", "3", "4"]:
				report_status = "3" 
			CdnNetInfo.objects.filter(id=tmp_id).update(
		        cdn_net_id = cdn_net_id,
		        cdn_top_domain = cdn_top_domain,
		        top_domain_record_num = top_domain_record_num,
		        report_status = report_status
		    )
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		return HttpResponseRedirect('/cdn_net_list') 

	def _add():
	    try:
	        CdnNetInfo.objects.create(
	            cdn_net_id = get_auto_16_id(),
	            cdn_top_domain = cdn_top_domain,
	            top_domain_record_num = top_domain_record_num,
	            report_status = "1"
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))
	    return HttpResponseRedirect('/cdn_net_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


def del_cdn_net(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}

	tmp_id = request.POST.get('id')

	# 后续添加的业务逻辑
	# 如果子网信息要删除，也要将子网下挂载的都进行删除

	try:
	    CdnNetInfo.objects.filter(id=tmp_id).delete()
	except:
	    return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))