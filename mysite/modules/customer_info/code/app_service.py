# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import AppServiceInfo, DomainInfo, CustomerInfo
from modules.share_part.share_func import *
from modules.dict_table.models import ServiceContent
from modules.dict_table.models import ReportStatus
from django.core.paginator import Paginator
import traceback
import json


# 获取应用服务信息
def app_service_list(request):
    try:
        # 按姓名查询
        if request.GET.get("customer_name"):
            customer_name = request.GET.get("customer_name")
            # 获取客户id
            _id = CustomerInfo.objects.get(unit_name=customer_name.strip()).id
            tmp_list = AppServiceInfo.objects.filter(customer_id_id=_id)
        elif request.GET.get("customer_id"):
            # 获取客户id
            tmp_list = AppServiceInfo.objects.filter(customer_id_id=request.GET['customer_id'])
        else:
            tmp_list = AppServiceInfo.objects.all()

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
            one.domain_info = get_domain_num(one.id)
            one.customer_name = CustomerInfo.objects.filter(id=one.customer_id_id)[0].unit_name
            one.service_content = get_china_service_content(one.service_content)
            one.report_status = get_dict_name(one.report_status, ReportStatus)
    except:
    	print(traceback.print_exc())
    return render_to_response('application_service.html', locals())


# 添加应用服务信息
def add_app_service(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        # 构建服务内容数据格式
        ret_list = parse_service_content()
        # 客户名称下拉
        customer_name_select = get_table_data(CustomerInfo)

        if request.GET.get("id"):
            tmp_id = request.GET.get("id")
            customer_id = AppServiceInfo.objects.get(id=tmp_id).customer_id_id
            edit_map = AppServiceInfo.objects.filter(id=tmp_id)[0]


            edit_map.service_content = json.loads(edit_map.service_content)
            edit_map.customer_name = get_name_byid_table(edit_map.customer_id_id, CustomerInfo).unit_name

            # 编辑时从下拉框中删除要编辑的，不然会显示重复
            customer_name_select = del_table_one_item(edit_map.customer_id_id, customer_name_select)
        return render_to_response('application_service_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    customer_id = request.POST.get("customer_id")
    service_content = get_service_content(request.POST)
    print("service_content:99999", service_content, type(service_content))


    def _update():
        try:
            AppServiceInfo.objects.filter(id=tmp_id).update(
                service_content = json.dumps(service_content),
                customer_id_id = customer_id,
                report_status = "3"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/app_service_list') 

    def _add():
        try:
            AppServiceInfo.objects.create(
                service_id = get_auto_16_id(),
                service_content = json.dumps(service_content),
                customer_id_id = customer_id,
                report_status = "1",
                report_time = "--"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/app_service_list')

    if request.method == "POST" and request.POST['id']:
        return _update()
    return _add()


# 删除应用服务信息
def del_app_service(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    tmp_id = request.POST.get("id")

    try:
        # 删除应用服务信息时会将它对应的域名信息也删除掉
        DomainInfo.objects.filter(app_service_id_id=tmp_id).delete()
        
        AppServiceInfo.objects.filter(id=tmp_id).delete()
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))


# 获取应用服务对应的域名数量
def get_domain_num(tmp_id=None):
    return DomainInfo.objects.filter(app_service_id_id=tmp_id).count()


# 组装服务内容数据格式供页面使用
# [{"key": "500", "value": "基础应用", "child": [{"1": u"即时通信"}, {"2": u"搜索引擎"}]},{}]
def parse_service_content():

    ret_list = list()
    parent_content = ServiceContent.objects.filter(parent_id="/")
    for one in parent_content:
        tmp_map = {
            "key": one.key,
            "value": one.value
        }
        ret_list.append(tmp_map)
    for i in ret_list:
        child = ServiceContent.objects.filter(parent_id=i["key"])
        i["child"] = child
        i["length"] = len(child)

    return ret_list


# 获取服务内容名称
def get_china_service_content(data=None):
    ret_string = ""
    data_list = json.loads(data)
    for one in data_list:
        x = get_dict_name(one, ServiceContent)
        ret_string +=  u"%s, " % x
    return ret_string[:-2]


# 处理页面提交的服务内容
def get_service_content(data=None):

    ret_list = list()
    parent_content = ServiceContent.objects.filter(parent_id="/")
    for one in parent_content:
        content = data.getlist(one.key, [])
        ret_list.extend(content)

    return ret_list