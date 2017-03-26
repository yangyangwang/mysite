# coding = utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from modules.share_part.share_func import get_cur_time, get_dict_name, return_msg
from ..models import MountCdnNode, CdnNetInfo
from modules.dict_table.models import ReportStatus
from modules.business_unit.models import BusinessUnit
from modules.cdn_node_info.models import CdnNodeInfo, MountCdnHouse
from config.config_parse import local_xml_path, local_xsd_path
from modules.cdn_node_house.models import CdnNodeHouse, HouseLink, HouseFrame, HouseIpseg
from xml.dom.minidom import Document
from modules.share_part.handle_xml import *
import traceback
import json


# cdn子网下挂载cdn节点
def mount_cdn_node(request):
    try:
        # 使用href 传过来的值多了空格值，长度变成了17位
        cdn_net_id = request.GET.get("cdn_net_id").strip()
        cdn_node_list = CdnNodeInfo.objects.all()
        length = CdnNodeInfo.objects.filter().count()

        # 获取挂载的节点信息
        has_mount_node = MountCdnNode.objects.filter(cdn_net_id=cdn_net_id)
        # 用于勾选框选中
        mount_node_list = [one.cdn_node_id for one in has_mount_node]
        # 用已经挂载的信息覆盖原来的信息
        if has_mount_node:
            for x in cdn_node_list:
                for y in has_mount_node:
                    if x.cdn_node_id == y.cdn_node_id:
                        x.mount_house = MountCdnHouse.objects.filter(cdn_node_id=x.cdn_node_id, cdn_net_id=cdn_net_id).count()
                        x.mount_report_status = get_dict_name(y.report_status, ReportStatus)
                        x.mount_report_time = y.report_time
                        x.mount_create_time = y.create_time
    except:
        print(traceback.print_exc())
    return render_to_response("mount_cdn_node.html", locals())


# 保存挂载信息
def save_mount_cdn_node(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}

    try:
        print(request.POST)
        cdn_net_id = request.POST.get("cdn_net_id").strip()
        cdn_node_id_list_str = request.POST.get("cdn_node_id_list")
        cdn_node_id_list = json.loads(cdn_node_id_list_str)
        cdn_node_id_list = list(filter(lambda x : x, cdn_node_id_list))

        # 获取先前挂载的节点
        before_mount_node = MountCdnNode.objects.filter(cdn_net_id=cdn_net_id)
        before_mount_node_id_list = [one.cdn_node_id for one in before_mount_node]

        # 找出新添加的节点信息
        new_mount_node = list(set(cdn_node_id_list).difference(set(before_mount_node_id_list)))

        # 新去掉的
        new_mount_node_bak = list(set(before_mount_node_id_list).difference(set(cdn_node_id_list)))
        if not new_mount_node:  # 没有新添加的，检查是否有删除的（并且是否是未上报的）
            if new_mount_node_bak:
                for one in new_mount_node_bak:
                    status_tmp = MountCdnNode.objects.get(cdn_node_id=one).report_status
                    if int(status_tmp) == 1:
                        MountCdnNode.objects.filter(cdn_node_id=one).delete()
                        # 删除子网下挂载的节点下挂载的机房信息
                        MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=one).delete()
            return HttpResponse(json.dumps(back_dict))


        if not new_mount_node:
            return HttpResponse(json.dumps(back_dict))


        cur_time = get_cur_time()
        # 挂载节点
        for one_node_id in new_mount_node:
            MountCdnNode.objects.create(
                    cdn_net_id = cdn_net_id,
                    cdn_node_id = one_node_id,
                    report_status = "1",
                    report_time = "--",
                    create_time = cur_time
                )

        # 将子网，节点，机房 三者之间的关系对应起来
        for one_node_id in new_mount_node:
            mount_house_list = MountCdnHouse.objects.filter(cdn_node_id=one_node_id, cdn_net_id=None)
            mount_house_id_list = [one.cdn_house_id for one in mount_house_list]
            for one_house_id in mount_house_id_list:
                MountCdnHouse.objects.create(
                    cdn_net_id = cdn_net_id,
                    cdn_node_id = one_node_id,
                    cdn_house_id = one_house_id,
                    report_status = "1",
                    report_time = "--",
                    create_time = cur_time
                )
        # 修改子网的状态为更新未上报
        net_status = CdnNetInfo.objects.get(cdn_net_id=cdn_net_id).report_status
        if int(net_status) in [2, 4]:
            CdnNetInfo.objects.filter(cdn_net_id=cdn_net_id).update(report_status="3")

    except:
        print(traceback.print_exc())
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))


# 上报cdn子网下挂载的节点信息
def report_mount_cdn_node(request):

    try:
        cdn_net_id = request.POST.get("cdn_net_id").strip()
        cdn_node_id = request.POST.get("cdn_node_id").strip()

        cdn_net_info = CdnNetInfo.objects.get(cdn_net_id=cdn_net_id)
        cdnNetId = cdn_net_id
        topDomain = cdn_net_info.cdn_top_domain
        regId = cdn_net_info.top_domain_record_num
        net_report_status = cdn_net_info.report_status

        # 挂载的cdn节点信息
        mount_node_id_list = MountCdnNode.objects.filter(cdn_node_id=cdn_node_id)
        report_status = MountCdnNode.objects.get(cdn_node_id=cdn_node_id).report_status

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        if int(report_status) == 1:  # 新增未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'newInfo')
            xml_file = local_xml_path + "/basic_add_mount_node_info.xml"
            xsd_file = local_xsd_path + "/basic_add_mount_node_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence
        cdnName = BusinessUnit.objects.all()[0].unit_name
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnId', cdnId)

        cdnNetInfo = xml_obj.create_child_node(doc, NodeInfo, 'cdnNetInfo')

        xml_obj.add_value_to_node(doc, cdnNetInfo, 'cdnNetId', cdnNetId)
        if int(net_report_status) == 1:
            xml_obj.add_value_to_node(doc, cdnNetInfo, 'topDomain', topDomain)
            xml_obj.add_value_to_node(doc, cdnNetInfo, 'regId', regId)

        if int(report_status) == 1:
            for one in mount_node_id_list:
                node = xml_obj.create_child_node(doc, cdnNetInfo, 'node')
                xml_obj.add_value_to_node(doc, node, 'nodeId', one.cdn_node_id)
                node_name = CdnNodeInfo.objects.get(cdn_node_id=one.cdn_node_id).cdn_node_name
                xml_obj.add_value_to_node(doc, node, 'nodeName', node_name)

                # 子网下挂载的节点下的机房
                mount_house_id_list = MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, 
                    cdn_node_id=one.cdn_node_id)
                for h in mount_house_id_list:
                    houseInfo = xml_obj.create_child_node(doc, node, 'houseInfo')
                    houseName = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).cdn_house_name
                    houseType = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).cdn_house_nature
                    houseProvince = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).house_province
                    houseCity = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).house_city
                    houseCounty = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).house_county
                    houseAdd = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).house_address
                    houseZip = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).house_zipcode
                    venderName = cdnName

                    xml_obj.add_value_to_node(doc, houseInfo, 'houseId', h.cdn_node_id)

                    xml_obj.add_value_to_node(doc, houseInfo, 'houseName', houseName)
                    xml_obj.add_value_to_node(doc, houseInfo, 'houseType', houseType)
                    xml_obj.add_value_to_node(doc, houseInfo, 'houseProvince', houseProvince)
                    xml_obj.add_value_to_node(doc, houseInfo, 'houseCity', houseCity)

                    xml_obj.add_value_to_node(doc, houseInfo, 'houseCounty', houseCounty)
                    xml_obj.add_value_to_node(doc, houseInfo, 'houseAdd', houseAdd)
                    if houseZip:
                        xml_obj.add_value_to_node(doc, houseInfo, 'houseZip', houseZip)
                    xml_obj.add_value_to_node(doc, houseInfo, 'venderName', venderName)

                    # 链路信息
                    house_id_id = CdnNodeHouse.objects.get(cdn_house_id=h.cdn_house_id).id
                    print("#####:", house_id_id)
                    gataway_info = HouseLink.objects.filter(house_id_id=house_id_id)

                    # 对应整形必须转为字符串才可以通过
                    for g in gataway_info:
                        gatewayInfo = xml_obj.create_child_node(doc, houseInfo, 'gatewayInfo')
                        xml_obj.add_value_to_node(doc, gatewayInfo, 'id', str(g.id))
                        xml_obj.add_value_to_node(doc, gatewayInfo, 'bandWidth', str(g.link_bandwidth))
                        xml_obj.add_value_to_node(doc, gatewayInfo, 'linkType', g.link_type)
                        xml_obj.add_value_to_node(doc, gatewayInfo, 'linkTime', g.link_time)

                    # 机架信息
                    frame_info = HouseFrame.objects.filter(house_id_id=house_id_id)

                    for f in frame_info:
                        frameInfo = xml_obj.create_child_node(doc, houseInfo, 'frameInfo')
                        xml_obj.add_value_to_node(doc, frameInfo, 'id', str(f.id))
                        xml_obj.add_value_to_node(doc, frameInfo, 'useType', f.use_type)
                        xml_obj.add_value_to_node(doc, frameInfo, 'frameName', f.frame_name)

                    # IP地址段信息
                    ipseg_info = HouseIpseg.objects.filter(house_id_id=house_id_id)

                    for i in ipseg_info:
                        ipSegInfo = xml_obj.create_child_node(doc, houseInfo, 'ipSegInfo')
                        xml_obj.add_value_to_node(doc, ipSegInfo, 'id', str(i.id))
                        xml_obj.add_value_to_node(doc, ipSegInfo, 'startIp', i.start_ip)
                        xml_obj.add_value_to_node(doc, ipSegInfo, 'endIp', i.end_ip)
                        xml_obj.add_value_to_node(doc, ipSegInfo, 'type', i.ip_use_type)

        timeStamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        xml_obj.add_value_to_node(doc, basicInfo, 'timeStamp', timeStamp)
            
        print("xml_file:", xml_file)
        # 写入xml文件
        with open(xml_file, "w") as f:
            doc.writexml(f, addindent=' ' * 4, newl='\n', encoding="UTF-8")

        # 利用xsd校验xml文件
        ret = check_xml_file(xsd_file, xml_file)
        if ret != 1:
            print("%s check Fail!!!" % xml_file)
            return return_msg(1)

        # FTP上报xml文件到管局
        return_code = ftp_report_mount_node(report_status, xml_file, cdn_node_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_report_mount_node(report_status, xml_file, cdn_node_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            tmp_status = "2"
            report_time = get_cur_time()
            # 如果子网的状态为新增未上报，更新子网上报状态
            cdn_net_id = MountCdnNode.objects.get(cdn_node_id=cdn_node_id).cdn_net_id
            net_report_status = CdnNetInfo.objects.get(cdn_net_id=cdn_net_id).report_status
            if int(net_report_status) == 1:
                CdnNetInfo.objects.filter(cdn_net_id=cdn_net_id).update(report_status=tmp_status, report_time=report_time)

            if int(report_status) == 1:
                # 更新挂载的节点上报状态
                MountCdnNode.objects.filter(cdn_node_id=cdn_node_id).update(report_status=tmp_status, report_time=report_time)
                # 更新子网下的节点下的机房上报状态
                MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=cdn_node_id).update(report_status=tmp_status, report_time=report_time)

                # 判断此节点是否已经上报过，如果没有上报过，修改其状态为新增已上报
                node_status = CdnNodeInfo.objects.get(cdn_node_id=cdn_node_id).report_status
                if int(node_status) == 1:
                    CdnNodeInfo.objects.filter(cdn_node_id=cdn_node_id).update(report_status=tmp_status, report_time=report_time)
                

                cdn_house = MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=cdn_node_id)

                for one in cdn_house:
                    # 判断此节点下的机房是否已经上报过，如果没有上报过，修改其状态为新增已上报
                    house_status = CdnNodeHouse.objects.get(cdn_house_id=one.cdn_house_id).report_status
                    if int(house_status) == 1:                  
                        CdnNodeHouse.objects.filter(cdn_house_id=one.cdn_house_id).update(report_status=tmp_status, report_time=report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2

