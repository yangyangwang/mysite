#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import DomainInfo, AppServiceInfo
from modules.share_part.share_func import *
from modules.dict_table.models import ReportStatus
from django.core.paginator import Paginator
import traceback
import json


# 获取应用服务对应的域名列表信息
def domain_info_list(request):
    try:
        # 按姓名查询
        if request.GET.get("domain"):
            domain = request.GET.get("domain")
            tmp_list = DomainInfo.objects.filter(domain=domain)
        elif request.GET.get("app_service_id"):
            tmp_list = DomainInfo.objects.filter(app_service_id_id=request.GET['app_service_id'])
        else:
            tmp_list = DomainInfo.objects.all()

        # 每页列表显示的数量，读配置文件获取
        PAGE_SIZE = 5
        page_size = PAGE_SIZE

        # 要获取的第几页数据，默认为第一页
        try:
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        # 创建分页对象
        paginator = Paginator(tmp_list, page_size)
        page_obj = paginator.page(page)

        for one in page_obj.object_list:
            one.report_status = get_dict_name(one.report_status, ReportStatus)
    except:
        print(traceback.print_exc())
    return render_to_response('domain_info_list.html', locals())


# 添加编辑域名信息
def add_domain_info(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}
    back_dict_service = {"code": 1, "msg": u"输入的服务编号不存在！"}

    def _get():
        app_service_id = request.GET.get("app_service_id")
        if request.GET.get("id"):
            tmp_id = request.GET.get("id")
            app_service_id = DomainInfo.objects.get(id=tmp_id).app_service_id_id
            edit_map = DomainInfo.objects.get(id = tmp_id)
            edit_map.service_id = AppServiceInfo.objects.get(id=edit_map.app_service_id_id).service_id
        return render_to_response('domain_info_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    service_id = request.POST.get("service_id")  # 服务编号
    # 校验服务编号是否存在, 放在前端校验以后，实时的校验
    try:
        service_info = AppServiceInfo.objects.get(service_id=service_id)
    except:
        return HttpResponse(json.dumps(back_dict_service))
        

    # 由服务编号获取服务id
    app_service_id = service_info.id

    domain = request.POST.get("domain")
    source_address = request.POST.get("source_address")
    record_num = request.POST.get("record_num")
    top_domain = request.POST.get("top_domain")
  

    def _update():
        try:
            DomainInfo.objects.filter(id=tmp_id).update(
                domain = domain,
                source_address = source_address,
                record_num = record_num,
                top_domain = top_domain,
                report_status = "3"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/domain_info_list')

    def _add():
        try:
            DomainInfo.objects.create(
                domain_id = get_auto_16_id(),
                domain = domain,
                source_address = source_address,
                record_num = record_num,
                top_domain = top_domain,
                app_service_id_id = int(app_service_id),
                report_status = "1",
                report_time = "--"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/domain_info_list')

    if request.method == "POST" and request.POST['id']:
        return _update()
    return _add()


# 删除域名信息
def del_domain_info(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}
    tmp_id = request.POST.get("id")

    # 此处操作是为了删除域名信息后，还可以在添加应用服务的域名，不然后导致app_service_id丢失
    app_service_id_id = DomainInfo.objects.get(id=tmp_id).app_service_id_id
    back_dict["app_service_id"] = app_service_id_id
    back_dict_err["app_service_id"] = app_service_id_id

    try:
        DomainInfo.objects.filter(id=int(tmp_id)).delete()
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))