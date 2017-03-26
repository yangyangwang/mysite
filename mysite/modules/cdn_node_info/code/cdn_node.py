#coding = utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from modules.cdn_node_house.models import CdnNodeHouse
from ..models import CdnNodeInfo, MountCdnHouse
from modules.dict_table.models import HouseNature, ReportStatus
from modules.business_unit.models import BusinessUnit
from modules.cdn_net_info.models import MountCdnNode, CdnNetInfo
from modules.network_manager.models import NetworkManager
from modules.share_part.share_func import get_cur_time, get_dict_name, get_name_byid_table
from modules.cdn_node_house.views import get_link_num, get_frame_num, get_ipseg_num
import traceback
import json


# cdn节点下挂载cdn机房
def mount_cdn_house(request):
    try:
        # 使用href 传过来的值多了空格值，长度变成了17位
        cdn_net_id = request.GET.get("cdn_net_id", "0").strip()
        cdn_node_id = request.GET.get("cdn_node_id").strip()
        cdn_node_name = CdnNodeInfo.objects.get(cdn_node_id=cdn_node_id).cdn_node_name
        cdn_house_list = CdnNodeHouse.objects.all()
        length = CdnNodeHouse.objects.filter().count()

        for one in cdn_house_list:
            # 机房属性
            one.cdn_house_nature = get_dict_name(one.cdn_house_nature, HouseNature)

            # 获取该机房的链路信息个数
            one.link_info = get_link_num(one.id)

            # 获取该机房的机架信息个数
            one.frame_info = get_frame_num(one.id)

            # 获取该机房的IP地址段信息个数
            one.ipseg_info = get_ipseg_num(one.id)

            one.network_people = get_name_byid_table(int(one.network_people), NetworkManager).name

            one.business_unit = get_name_byid_table(int(one.business_unit), BusinessUnit).unit_name


        # 获取挂载的机房信息
        if cdn_net_id == "0":
            has_mount_house = MountCdnHouse.objects.filter(cdn_node_id=cdn_node_id, cdn_net_id=None)
        else:
            has_mount_house = MountCdnHouse.objects.filter(cdn_node_id=cdn_node_id, cdn_net_id=cdn_net_id)
        # 用于勾选框选中
        mount_house_list = [one.cdn_house_id for one in has_mount_house]
        if cdn_net_id and has_mount_house:
            for x in cdn_house_list:
                for y in has_mount_house:
                    if x.cdn_house_id == y.cdn_house_id:
                        x.mount_report_status = get_dict_name(y.report_status, ReportStatus)
                        x.mount_report_time = y.report_time
                        x.mount_create_time = y.create_time
    except:
        print(traceback.print_exc())
    return render_to_response("mount_cdn_house.html", locals())


# 保存挂载信息
def save_mount_cdn_house(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}

    try:
        print(request.POST)
        cdn_node_id = request.POST.get("cdn_node_id").strip()
        cdn_house_id_list_str = request.POST.get("cdn_house_id_list")
        cdn_house_id_list = json.loads(cdn_house_id_list_str)
        cdn_house_id_list = list(filter(lambda x : x, cdn_house_id_list))

        # 判断此节点是否已经被子网进行挂载了。没有挂载，就进行删除后添加。
        is_mount_by_net = MountCdnNode.objects.filter(cdn_node_id=cdn_node_id)
        if not is_mount_by_net:
            MountCdnHouse.objects.filter(cdn_node_id=cdn_node_id, cdn_net_id=None).delete()

        # 获取先前挂载的机房
        before_mount_house = MountCdnHouse.objects.filter(cdn_net_id=None, cdn_node_id=cdn_node_id)
        before_mount_house_id_list = [one.cdn_house_id for one in before_mount_house]

        # 找出新添加的节点信息
        new_mount_house = list(set(cdn_house_id_list).difference(set(before_mount_house_id_list)))

        # 暂时先不考虑去掉一个新添加的没有上报的机房。
        cur_time = get_cur_time()
        for one in new_mount_house:
            MountCdnHouse.objects.create(
                cdn_node_id = cdn_node_id,
                cdn_house_id = one.strip(),
                create_time = cur_time
            )
        # 将新添加的机房都挂载子网下
        if is_mount_by_net:
            cdn_net_info = MountCdnNode.objects.filter(cdn_node_id=cdn_node_id)
            # 建立子网，节点，机房三者的关系，表示新添加的机房挂载子网下
            for O in cdn_net_info:
                for one_cdn_house_id in new_mount_house:
                    MountCdnHouse.objects.create(
                        cdn_net_id = O.cdn_net_id,
                        cdn_node_id = cdn_node_id,
                        cdn_house_id = one_cdn_house_id.strip(),
                        report_status = "1",
                        report_time = cur_time,
                        create_time = cur_time
                    )
            # 更新子网下挂载的节点的状态为新增未上报
            MountCdnNode.objects.filter(cdn_node_id=cdn_node_id).update(report_status="1")
            # 更新子网的状态
            for H in cdn_net_info:
                net_status = CdnNetInfo.objects.get(cdn_net_id=H.cdn_net_id).report_status
                if int(net_status) not in [1, 3]:
                    CdnNetInfo.objects.filter(cdn_net_id=H.cdn_net_id).update(report_status="3")
    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))