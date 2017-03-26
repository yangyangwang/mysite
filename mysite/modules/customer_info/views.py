# coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import CustomerInfo, AppServiceInfo, DomainInfo
from ..business_unit.models import BusinessUnit
from ..network_manager.models import NetworkManager
from ..share_part.share_func import *
from ..dict_table.models import ServiceContent
from ..dict_table.models import UnitNature, IdType, ReportStatus
from django.core.paginator import Paginator
import traceback
import json


# Create your views here.
# 获取客户信息列表
def customer_info_list(request):
    # 按单位名称查询
    if request.GET.get("unit_name"):
        unit_name = request.GET.get("unit_name")
        tmp_list = CustomerInfo.objects.filter(unit_name=unit_name.strip())
    else:
        tmp_list = CustomerInfo.objects.all()

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
        one.app_service = get_app_service_num(one.id)
        one.id_type = get_dict_name(one.id_type, IdType)
        one.unit_nature = get_dict_name(one.unit_nature, UnitNature)
        one.network_people = get_name_byid_table(int(one.network_people), NetworkManager).name
        one.report_status = get_dict_name(one.report_status, ReportStatus)
        
    return render_to_response('customer_info_list.html', locals())


# 获取客户下的服务信息个数
def get_app_service_num(tmp_id=None):
    return AppServiceInfo.objects.filter(customer_id_id=tmp_id).count()


# 添加编辑客户信息
def add_customer_info(request):
    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        # 单位属性下拉
        unit_nature_select = get_table_data(UnitNature)

        # 证件类型下拉
        id_type_select = get_table_data(IdType)

        # 网络负责人下拉
        network_people_select = get_table_data(NetworkManager)

        # 所属经营者单位下拉
        business_unit_select = get_table_data(BusinessUnit)

        if request.GET.get('id'):  # 表示获取要编辑的数据
            edit_map = CustomerInfo.objects.filter(id = request.GET['id'])[0]
            edit_map.unit_nature_name = get_dict_name(edit_map.unit_nature, UnitNature)
            edit_map.id_type_name = get_dict_name(edit_map.id_type, IdType)
            edit_map.network_people_name = get_name_byid_table(edit_map.network_people, NetworkManager).name
            edit_map.business_unit_name = get_name_byid_table(edit_map.business_unit, BusinessUnit).unit_name
            
            # 从下拉框中过滤掉要编辑的数据
            unit_nature_select = del_dict_one_item(edit_map.unit_nature, unit_nature_select)
            id_type_select = del_dict_one_item(edit_map.id_type, id_type_select)
            network_people_select = del_table_one_item(edit_map.network_people, network_people_select)
            business_unit_select = del_table_one_item(edit_map.business_unit, business_unit_select)


        return render_to_response('customer_info_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    # 下面表示post请求
    tmp_id = request.POST.get('id')
    unit_name = request.POST.get('unit_name')
    unit_address = request.POST.get('unit_address')
    unit_zipcode = request.POST.get('unit_zipcode')
    unit_nature = request.POST.get('unit_nature')
    id_type = request.POST.get('id_type')
    id_no = request.POST.get('id_no')
    network_people = request.POST.get('network_people')
    register_time = request.POST.get('register_time')
    business_unit = request.POST.get('business_unit')

    # 从页面取到的数据是字符串类型的

    def _update():
        try:
            CustomerInfo.objects.filter(id=tmp_id).update(
                unit_name = unit_name,
                unit_address = unit_address,
                unit_zipcode = unit_zipcode,
                unit_nature = unit_nature,
                id_type = id_type,
                id_no = id_no,
                network_people = int(network_people),
                register_time = register_time,
                business_unit = int(business_unit),
                report_status = "3",
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/customer_info_list') 

    def _add():
        try:
            CustomerInfo.objects.create(
                customer_id = get_auto_16_id(),
                unit_name = unit_name,
                unit_address = unit_address,
                unit_zipcode = unit_zipcode,
                unit_nature = unit_nature,
                id_type = id_type,
                id_no = id_no,
                network_people = int(network_people),
                register_time = register_time,
                business_unit = int(business_unit),
                report_status = "1",
                report_time = "--"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/customer_info_list')

    if request.method == "POST" and request.POST['id']:
        return _update()
    return _add()


# 删除客户信息
def del_customer_info(request):
    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    tmp_id = request.POST.get("id")
    try:
        # 删除客户信息时先删除客户的服务下的域名，再删服务，再删客户
        service_info = AppServiceInfo.objects.filter(customer_id_id=tmp_id)
        
        # 删除每个服务下的域名信息
        for one in service_info:
            DomainInfo.objects.filter(app_service_id_id=one.id).delete()

        # 删除服务
        AppServiceInfo.objects.filter(customer_id_id=tmp_id)

        # 删除客户
        CustomerInfo.objects.filter(id=tmp_id).delete()
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))


# 获取服务内容名称
def get_china_service_content(data=None):
    ret_string = ""
    data_list = json.loads(data)
    for one in data_list:
        x = get_dict_name(one, ServiceContent)
        ret_string +=  u"%s, " % x
    return ret_string


# 获取应用服务信息
def app_service_list(request):

    customer_id = request.GET.get("customer_id")
    if not customer_id:
        # 当添加保存后，会重定向导致house_id丢失。此时从session中获取
        customer_id = request.session.get("customer_id")
    
    ret_list = AppServiceInfo.objects.filter(customer_id_id=customer_id)
    for one in ret_list:
        one.domain_info = get_domain_num(one.id)
        one.service_content = get_china_service_content(one.service_content)
    return render_to_response('application_service.html', locals())


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


# 处理页面提交的服务内容
def get_service_content(data=None):

    ret_list = list()
    parent_content = ServiceContent.objects.filter(parent_id="/")
    for one in parent_content:
        content = data.getlist(one.key, [])
        ret_list.extend(content)

    return ret_list


# 添加应用服务信息
def add_app_service(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        customer_id = request.GET.get("customer_id")
        # 构建服务内容数据格式
        ret_list = parse_service_content()
        if request.GET.get("id"):
            tmp_id = request.GET.get("id")
            customer_id = AppServiceInfo.objects.get(id=tmp_id).customer_id_id
            edit_map = AppServiceInfo.objects.filter(id=tmp_id)[0]

            edit_map.service_content = json.loads(edit_map.service_content)
            print(edit_map)
        return render_to_response('application_service_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    service_content = get_service_content(request.POST)
    print("service_content:99999", service_content, type(service_content))
    customer_id = request.POST.get("customer_id")


    def _update():
        try:
            AppServiceInfo.objects.filter(id=tmp_id).update(
                service_content = service_content,
                report_status = "3"
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/customer_info_list') 

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
        request.session["customer_id"] = customer_id
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


# 获取应用服务对应的域名列表信息
def domain_info_list(request):

    try:
        app_service_id = request.GET.get("app_service_id")
        ret_list = DomainInfo.objects.filter(app_service_id=int(app_service_id))
    except:
        print(traceback.print_exc())
    return render_to_response('domain_info_list.html', locals())


# 添加编辑域名信息
def add_domain_info(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        app_service_id = request.GET.get("app_service_id")
        if request.GET.get("id"):
            tmp_id = request.GET.get("id")
            app_service_id = DomainInfo.objects.get(id=tmp_id).app_service_id_id
            edit_map = DomainInfo.objects.get(id = tmp_id)
        return render_to_response('domain_info_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    app_service_id = request.POST.get("app_service_id")
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
        return HttpResponseRedirect('/domain_info_list?app_service_id= + %s' % app_service_id)

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
        return HttpResponseRedirect('/domain_info_list?app_service_id= + %s' % app_service_id)

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