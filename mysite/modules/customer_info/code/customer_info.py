# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import CustomerInfo, AppServiceInfo, DomainInfo
from modules.business_unit.models import BusinessUnit
from modules.network_manager.models import NetworkManager
from modules.share_part.share_func import *
from modules.dict_table.models import UnitNature, IdType, ReportStatus
from django.core.paginator import Paginator
import traceback
import json



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

