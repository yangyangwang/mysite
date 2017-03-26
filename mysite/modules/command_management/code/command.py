# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from modules.business_unit.models import BusinessUnit
from modules.share_part.share_func import get_cur_time
from django.core.paginator import Paginator
from ..models import Command
from modules.share_part.share_func import get_table_data, get_dict_name, del_dict_one_item
from modules.dict_table.models import CommandType, CommandOperateType, RuleType
from modules.cdn_node_house.models import CdnNodeHouse
import traceback
import json


def command_list(request):
    try:
        if request.GET.get("command_id"):
            command_id = request.GET.get("command_id")
            tmp_list = Command.objects.filter(command_id=int(command_id))
        else:
            tmp_list = Command.objects.all()

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
            one.command_type = get_dict_name(one.command_type, CommandType)
            one.operate_type = get_dict_name(one.operate_type, CommandOperateType)
            one.unit_licence = BusinessUnit.objects.get(unit_licence=one.unit_licence).unit_name
            one.house = get_house_china_name(one.house)
    except:
        print(traceback.print_exc())
    return render_to_response("command_list.html", locals())


# 获取机房称
def get_house_china_name(data=None):
    ret_string = ""
    data_list = json.loads(data)
    for one in data_list:
        x = CdnNodeHouse.objects.get(id=int(one)).cdn_house_name
        ret_string +=  u"%s, " % x
    return ret_string[:-2]
    

# 添加指令
def add_command(request):

    back_dict = {"code": 0, "msg": "success"}
    back_dict_err = {"code": 1, "msg": "error"}

    def _get():
        try:
            # 管理指令类型下拉
            command_type_select = get_table_data(CommandType)
            # 操作类型下拉
            operate_type_select = get_table_data(CommandOperateType)
            # 规则类型下拉
            rule_type_select = get_table_data(RuleType)
            # 机房列表
            house_list = CdnNodeHouse.objects.all()
            for one in house_list:
                # 为了和选中的机房中的id对应，那里是字符串类型，不然页面的勾选不能回显。
                one.id = str(one.id)

            if request.GET.get('id'):  # 表示获取要编辑的数据
                edit_map = Command.objects.get(id = request.GET['id'])

                edit_map.command_type_name = get_dict_name(edit_map.command_type, CommandType)
                edit_map.operate_type_name = get_dict_name(edit_map.operate_type, CommandOperateType)
                edit_map.rule_type_name = get_dict_name(edit_map.rule_type, RuleType)
                edit_map.house = json.loads(edit_map.house)
                edit_map.keyword = json.loads(edit_map.keyword)
                
                # 从下拉框中过滤掉要编辑的数据
                command_type_select = del_dict_one_item(edit_map.command_type, command_type_select)
                operate_type_select = del_dict_one_item(edit_map.operate_type, operate_type_select)
                rule_type_select = del_dict_one_item(edit_map.rule_type, rule_type_select)
        except:
            print(traceback.print_exc())        
        return render_to_response('command_edit.html', locals())

    if request.method == "GET":
        return _get()

    print("#####################################")
    print(request.POST)
    print("#####################################")

    tmp_id = request.POST.get("id")
    command_id = request.POST.get("command_id")
    print("command_id", command_id, type(command_id))
    command_type = request.POST.get("command_type")
    operate_type = request.POST.get("operate_type")
    effect_time = request.POST.get("effect_time")
    deadline = request.POST.get("deadline")
    house = request.POST.getlist("house", [])

    if request.POST.get("is_write_log", ""):
        is_write_log = "1"  # 写日志
    else:
        is_write_log = "0"  # 不写日志
    if request.POST.get("is_report", ""):
        is_report = "1"  # 上报
    else:
        is_report = "0"  # 不上报

    filter_reason = request.POST.get("filter_reason")
    rule_type = request.POST.get("rule_type")
    rule_start_value = request.POST.get("rule_start_value")
    rule_end_value = request.POST.get("rule_end_value")
    keyword = request.POST.getlist("keyword", [])

    # 获取登录账号名
    unit_licence = BusinessUnit.objects.all()[0].unit_licence
    send_user = "admintest"
    create_time = get_cur_time()
    command_origin = "企侧"
    # 指令优先级（2048-4095）通过不同的规则类型进行划分
    priority = 3088


    def _update():
        try:
            Command.objects.filter(id=tmp_id).update(
                command_type = command_type,
                operate_type = operate_type,
                effect_time = effect_time,
                send_user = send_user,
                deadline = deadline,
                unit_licence = unit_licence,
                house = json.dumps(house),
                priority = priority,
                command_origin = command_origin,
                is_write_log = is_write_log,
                is_report = is_report,
                filter_reason = filter_reason,
                rule_type = rule_type,
                rule_start_value = rule_start_value,
                rule_end_value = rule_end_value,
                keyword = json.dumps(keyword),
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/command_list')

    def _add():
        try:
            Command.objects.create(
                command_id = int(command_id),
                command_type = command_type,
                operate_type = operate_type,
                effect_time = effect_time,
                send_user = send_user,
                deadline = deadline,
                unit_licence = unit_licence,
                house = json.dumps(house),
                priority = priority,
                command_origin = command_origin,
                is_write_log = is_write_log,
                is_report = is_report,
                filter_reason = filter_reason,
                rule_type = rule_type,
                rule_start_value = rule_start_value,
                rule_end_value = rule_end_value,
                keyword = keyword,
                create_time = create_time,
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/command_list')

    if request.method == "POST" and request.POST['id']:
        return _update()
    return _add()


# 删除指令
def del_command(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}
    tmp_id = request.POST.get("id")

    try:
        Command.objects.filter(id=int(tmp_id)).delete()
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))