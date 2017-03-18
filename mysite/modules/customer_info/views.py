# coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import CustomerInfo, AppServiceInfo, DomainInfo
from ..business_unit.models import BusinessUnit
from ..network_manager.models import NetworkManager
from ..share_part.share_func import *
from ..dict_table.models import UnitNature, IdType, ReportStatus
import traceback
import json


# Create your views here.
# 获取客户信息列表
def customer_info_list(request):
    ret_list = CustomerInfo.objects.all()
    if ret_list:
        for one in ret_list:
            one.app_service = get_app_service_num(one.id)
            one.id_type = get_dict_name(one.id_type, IdType)
            one.unit_nature = get_dict_name(one.unit_nature, UnitNature)
            one.network_people = get_name_byid_table(int(one.network_people), NetworkManager).name
            one.status = get_dict_name(one.status, ReportStatus)
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

    # 客户下应用服务信息的个数
    status = "1"

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
                business_unit = int(business_unit)
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/customer_info_list') 

    def _add():
        try:
            CustomerInfo.objects.create(
                unit_name = unit_name,
                unit_address = unit_address,
                unit_zipcode = unit_zipcode,
                unit_nature = unit_nature,
                id_type = id_type,
                id_no = id_no,
                network_people = int(network_people),
                register_time = register_time,
                business_unit = int(business_unit),
                status = status
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
        CustomerInfo.objects.filter(id=tmp_id).delete()
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))


# 获取应用服务信息
def app_service_list(request):

    customer_id = request.GET.get("customer_id")
    if not customer_id:
        # 当添加保存后，会重定向导致house_id丢失。此时从session中获取
        customer_id = request.session.get("customer_id")
    
    ret_list = AppServiceInfo.objects.filter(customer_id_id=customer_id)
    for one in ret_list:
        one.domain_info = get_domain_num(one.id)
    return render_to_response('application_service.html', locals())


# 获取应用服务对应的域名数量
def get_domain_num(tmp_id=None):
    return DomainInfo.objects.filter(app_service_id_id=tmp_id).count()


# 添加应用服务信息
def add_app_service(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        customer_id = request.GET.get("customer_id")
        return render_to_response('application_service_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    service_content = request.POST.get("service_content", '["1", "2"]')
    customer_id = request.POST.get("customer_id")


    def _update():
        try:
            AppServiceInfo.objects.filter(id=tmp_id).update(
                unit_name = unit_name,
                unit_address = unit_address,
                unit_zipcode = unit_zipcode,
                unit_nature = unit_nature,
                id_type = id_type,
                id_no = id_no,
                network_people = int(network_people),
                register_time = register_time,
                business_unit = int(business_unit)
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/customer_info_list') 

    def _add():
        try:
            AppServiceInfo.objects.create(
                service_id = get_auto_16_id(),
                service_content = service_content,
                customer_id_id = customer_id,
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
                top_domain = top_domain
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
                app_service_id_id = int(app_service_id)
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