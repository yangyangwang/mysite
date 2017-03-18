# coding=utf-8

import json
import traceback
from .models import NetworkManager
from ..business_unit.models import BusinessUnit
from django.shortcuts import render_to_response
from ..share_part.share_func import *
from ..dict_table.models import IdType
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect


# Create your views here.
def network_manager_list(request):
    ret_list = NetworkManager.objects.all()
    for one in ret_list:
        one.id_type = get_dict_name(one.id_type, IdType)
    return render_to_response('network_manager_list.html', locals())


# 添加编辑网络负责人信息
def add_network_manager(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "save error"}

    def _get():

        # 获取下拉框中的数据
        select_item_list = get_table_data(IdType)

        if request.GET.get('id', None):  # 表示获取要编辑的数据
            edit_map = NetworkManager.objects.filter(id = request.GET['id'])[0]
            edit_map.id_type_name = get_dict_name(edit_map.id_type, IdType)

            # 过滤掉字典表列表中的选中项
            select_item_list = del_dict_one_item(edit_map.id_type, select_item_list)
        return render_to_response('network_manager_edit.html', locals())

    if request.method == "GET":
        return _get()

    # 下面表示post请求
    print("===================================")
    print(request.POST)
    print("===================================")
        
    tmp_id = request.POST.get('id')
    name = request.POST.get('name')
    id_type = request.POST.get('id_type')
    id_number = request.POST.get('id_number')
    tel = request.POST.get('tel')
    phone = request.POST.get('phone')
    email = request.POST.get('email')

    def _update():
        try:
            NetworkManager.objects.filter(id=tmp_id).update(
                name=name,
                id_type=id_type,
                id_number=id_number,
                tel=tel,
                phone=phone,
                email=email
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/network_manager_list') 

    def _add():
        try:
            NetworkManager.objects.create(
                name=name,
                id_type=id_type,
                id_number=id_number,
                tel=tel,
                phone=phone,
                email=email
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/network_manager_list') 

    if request.method == "POST" and request.POST['id']:
        return _update()
    return _add()


# 删除网络负责人信息
# 如果网络负责人被应用就不能被删除
def del_network_manager(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}
    back_dict_nodel = {"code": "2", "msg": u"改信息已被经营者单位应用，误删！"}

    tmp_id = request.POST.get('id')

    # 查询经营者单位有没有应用该网络负责人
    if BusinessUnit.objects.filter(netinfo_people=tmp_id) or \
            BusinessUnit.objects.filter(emergency_people=tmp_id):
        return HttpResponse(json.dumps(back_dict_nodel))

    try:
        NetworkManager.objects.filter(id=tmp_id).delete()
    except:
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))



