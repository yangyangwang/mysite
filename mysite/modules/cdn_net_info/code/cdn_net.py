#coding = utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from modules.share_part.share_func import *
from modules.dict_table.models import ReportStatus
from modules.cdn_node_info.models import MountCdnHouse, CdnNodeInfo
from modules.business_unit.models import BusinessUnit
from ..models import CdnNetInfo, MountCdnNode, MountCdnDomain
from config.config_parse import local_xml_path, local_xsd_path
from xml.dom.minidom import Document
from modules.cdn_node_house.models import CdnNodeHouse, HouseLink, HouseFrame, HouseIpseg
from modules.share_part.share_func import return_msg, get_cur_time
from modules.share_part.handle_xml import *
import traceback
import json


# 获取cdn子网列表信息
def cdn_net_list(request):
    ret_list = CdnNetInfo.objects.all()
    if ret_list:
        for one in ret_list:
            one.mount_node = MountCdnNode.objects.filter(cdn_net_id=one.cdn_net_id).count()
            one.mount_domain = MountCdnDomain.objects.filter(cdn_net_id=one.cdn_net_id).count()
            one.report_status = get_dict_name(one.report_status, ReportStatus)
    return render_to_response("cdn_net_info_list.html", locals())


# 添加编辑cdn子网信息
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


# 删除cdn子网信息
def del_cdn_net(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}

    tmp_id = request.POST.get('id')

    # 后续添加的业务逻辑
    # 如果子网信息要删除，也要将子网下挂载的都进行删除
    try:
        # 删除子网下挂载的节点
        MountCdnNode.objects.filter(cdn_net_id=tmp_id).delete()

        # 删除子网下挂载的域名
        MountCdnDomain.objects.filter(cdn_net_id=tmp_id).delete()
        # 删除子网
        CdnNetInfo.objects.filter(id=tmp_id).delete()
    except:
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))



# 上报cdn子网信息
def report_cdn_net(request):

    try:
        tmp_id = request.POST.get("id").strip()

        cdn_net_info = CdnNetInfo.objects.get(id=tmp_id)
        cdn_net_id = cdn_net_info.cdn_net_id
        
        cdnNetId = cdn_net_info.cdn_net_id
        topDomain = cdn_net_info.cdn_top_domain
        regId = cdn_net_info.top_domain_record_num
        report_status = cdn_net_info.report_status

        # 挂载的cdn节点信息
        mount_node_id_list = MountCdnNode.objects.filter(cdn_net_id=cdn_net_id, report_status="1")

        # 挂载的cdn加速域名信息
        mount_domain_id_list = MountCdnDomain.objects.filter(cdn_net_id=cdn_net_id, report_status="1")

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        if int(report_status) == 1:  # 新增未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'newInfo')
            xml_file = local_xml_path + "/basic_add_cdn_net_info.xml"
            xsd_file = local_xsd_path + "/basic_add_cdn_net_info.xsd"
        elif int(report_status) == 3:  # 更新未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
            xml_file = local_xml_path + "/basic_update_cdn_net_info.xml"
            xsd_file = local_xsd_path + "/basic_update_cdn_net_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence
        cdnName = BusinessUnit.objects.all()[0].unit_name
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnId', cdnId)

        cdnNetInfo = xml_obj.create_child_node(doc, NodeInfo, 'cdnNetInfo')

        xml_obj.add_value_to_node(doc, cdnNetInfo, 'cdnNetId', cdnNetId)
        xml_obj.add_value_to_node(doc, cdnNetInfo, 'topDomain', topDomain)
        xml_obj.add_value_to_node(doc, cdnNetInfo, 'regId', regId)

        # 当只有新增上报的时候，才报子网下挂载的信息。如果子网下挂载的节点，域名有变化，单独上报。
        # 更新上报只是针对子网自己的信息变化了。不包含挂载的节点，域名
        if int(report_status) in [1, 3]:
            if mount_node_id_list:  # 表示有新添加的节点或机房
                for one in mount_node_id_list:
                    node = xml_obj.create_child_node(doc, cdnNetInfo, 'node')
                    xml_obj.add_value_to_node(doc, node, 'nodeId', one.cdn_node_id)
                    node_name = CdnNodeInfo.objects.get(cdn_node_id=one.cdn_node_id).cdn_node_name
                    xml_obj.add_value_to_node(doc, node, 'nodeName', node_name)

                    # 子网下挂载的节点下的机房
                    mount_house_id_list = MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, 
                        cdn_node_id=one.cdn_node_id, report_status="1")
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

                        xml_obj.add_value_to_node(doc, houseInfo, 'houseId', h.cdn_house_id)

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
                        if not gataway_info:
                            print("gataway_info is null!")
                            return return_msg(4)

                        # 对应整形必须转为字符串才可以通过
                        for g in gataway_info:
                            gatewayInfo = xml_obj.create_child_node(doc, houseInfo, 'gatewayInfo')
                            xml_obj.add_value_to_node(doc, gatewayInfo, 'id', str(g.id))
                            xml_obj.add_value_to_node(doc, gatewayInfo, 'bandWidth', str(g.link_bandwidth))
                            xml_obj.add_value_to_node(doc, gatewayInfo, 'linkType', g.link_type)
                            xml_obj.add_value_to_node(doc, gatewayInfo, 'linkTime', g.link_time)

                        # 机架信息
                        frame_info = HouseFrame.objects.filter(house_id_id=house_id_id)
                        if not frame_info:
                            print("frame_info is null!")
                            return return_msg(4)

                        for f in frame_info:
                            frameInfo = xml_obj.create_child_node(doc, houseInfo, 'frameInfo')
                            xml_obj.add_value_to_node(doc, frameInfo, 'id', str(f.id))
                            xml_obj.add_value_to_node(doc, frameInfo, 'useType', f.use_type)
                            xml_obj.add_value_to_node(doc, frameInfo, 'frameName', f.frame_name)

                        # IP地址段信息
                        ipseg_info = HouseIpseg.objects.filter(house_id_id=house_id_id)
                        if not ipseg_info:
                            print("ipseg_info is null!")
                            return return_msg(4)

                        for i in ipseg_info:
                            ipSegInfo = xml_obj.create_child_node(doc, houseInfo, 'ipSegInfo')
                            xml_obj.add_value_to_node(doc, ipSegInfo, 'id', str(i.id))
                            xml_obj.add_value_to_node(doc, ipSegInfo, 'startIp', i.start_ip)
                            xml_obj.add_value_to_node(doc, ipSegInfo, 'endIp', i.end_ip)
                            xml_obj.add_value_to_node(doc, ipSegInfo, 'type', i.ip_use_type)
            if mount_domain_id_list:           
                for d in mount_domain_id_list:
                    xml_obj.add_value_to_node(doc, cdnNetInfo, 'domainId', d.cdn_domain_id)

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
        return_code = ftp_report_cdn_net(report_status, xml_file, cdn_net_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_report_cdn_net(report_status, xml_file, cdn_net_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            tmp_status = "2" if int(report_status) == 1 else "4"
            report_time = get_cur_time()
            # 更新子网上报状态
            CdnNetInfo.objects.filter(cdn_net_id=cdn_net_id).update(report_status=tmp_status, report_time=report_time)

            if int(report_status) in [1, 3]:
                # 更新挂载的节点上报状态
                MountCdnNode.objects.filter(cdn_net_id=cdn_net_id, report_status="1").update(report_status="2", report_time=report_time)
                # 更新子网下的节点下的机房上报状态
                MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, report_status="1").update(report_status="2", report_time=report_time)

                # 更新挂载的域名上报状态
                MountCdnDomain.objects.filter(cdn_net_id=cdn_net_id, report_status="1").update(report_status="2", report_time=report_time)

                cdn_node = MountCdnNode.objects.filter(cdn_net_id=cdn_net_id)
                # 更新节点自己也为已上报
                for one in cdn_node:
                    node_status = CdnNodeInfo.objects.get(cdn_node_id=one.cdn_node_id).report_status
                    if int(node_status) == 1:
                        CdnNodeInfo.objects.filter(cdn_node_id=one.cdn_node_id).update(report_status="2", report_time=report_time)
                    # 更新机房自己也为已上报
                    cdn_house = MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=one.cdn_node_id)
                    for h in cdn_house:                  
                        CdnNodeHouse.objects.filter(cdn_house_id=h.cdn_house_id, report_status="1").update(report_status="2", report_time=report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2


# 注销cdn子网信息
def logout_cdn_net(request):
    try:
        print("############################")
        print(request.POST)
        cdn_net_id = request.POST.get("cdn_net_id", "").strip()
        cdn_node_id = request.POST.get("cdn_node_id", "").strip()
        cdn_house_id = request.POST.get("cdn_house_id", "").strip()
        cdn_domain_id = request.POST.get("cdn_domain_id", "").strip()
        # flag 表示注销子网信息，节点信息，机房，域名信息中的那一个
        flag = request.POST.get("flag")

        if flag == "net":
            xml_file = local_xml_path + "/basic_delete_cdn_net_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_cdn_net_info.xsd"
        elif flag == "node":
            node_info = CdnNodeInfo.objects.get(cdn_node_id=cdn_node_id)
            xml_file = local_xml_path + "/basic_delete_node_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_node_info.xsd"
        elif flag == "house":
            xml_file = local_xml_path + "/basic_delete_house_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_house_info.xsd"
        elif flag == "domain":
            xml_file = local_xml_path + "/basic_delete_speed_domain_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_speed_domain_info.xsd"
        else:
            return return_msg(4)  

        cdnId = BusinessUnit.objects.all()[0].unit_licence

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        deleteInfo = xml_obj.create_child_node(doc, basicInfo, 'deleteInfo')
        xml_obj.add_value_to_node(doc, deleteInfo, 'cdnId', cdnId)

        cdnnetDeleteList = xml_obj.create_child_node(doc, deleteInfo, 'cdnnetDeleteList')
        xml_obj.add_value_to_node(doc, cdnnetDeleteList, 'cdnNetId', cdn_net_id)
        # 注销服务或域名信息
        if flag == "net":
            pass
        elif flag == "node":
            nodeDeleteList = xml_obj.create_child_node(doc, cdnnetDeleteList, 'nodeDeleteList')
            xml_obj.add_value_to_node(doc, nodeDeleteList, 'nodeId', cdn_node_id)
        elif flag == "house":
            nodeDeleteList = xml_obj.create_child_node(doc, cdnnetDeleteList, 'nodeDeleteList')
            xml_obj.add_value_to_node(doc, nodeDeleteList, 'nodeId', cdn_node_id)
            houseDeleteList = xml_obj.create_child_node(doc, nodeDeleteList, 'nodeDeleteList')
            xml_obj.add_value_to_node(doc, houseDeleteList, 'houseId', cdn_house_id)
        elif flag == "domain":
            xml_obj.add_value_to_node(doc, cdnnetDeleteList, 'domainId', cdn_domain_id)
           

        xml_obj.add_value_to_node(doc, deleteInfo, 'timeStamp', get_cur_time())
        xml_obj.add_value_to_node(doc, basicInfo, 'timeStamp', get_cur_time())

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
        return_code = ftp_logout_customer_info(xml_file,flag, cdn_net_id, 
            cdn_node_id, cdn_house_id, cdn_domain_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_logout_customer_info(xml_file, flag, cdn_net_id, 
            cdn_node_id, cdn_house_id, cdn_domain_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            if flag == "net":
                report_time = get_cur_time()
                CdnNetInfo.objects.filter(cdn_net_id=cdn_net_id).update(report_status="5", report_time=report_time)

                # 删除子网下挂载的节点
                MountCdnNode.objects.filter(cdn_net_id=cdn_net_id).delete()
                # 删除子网下挂载的机房
                MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id).delete()
                # 删除子网本身
                CdnNetInfo.objects.filter(cdn_net_id=cdn_net_id).delete()
            elif flag == "node":
                # 删除子网下挂载的节点
                MountCdnNode.objects.filter(cdn_node_id=cdn_node_id, cdn_net_id=cdn_net_id).delete()
                # 删除子网下挂载的节点下的机房
                MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=cdn_node_id).delete()
            elif flag == "house":
                # 删除子网下挂载的节点下的机房
                MountCdnHouse.objects.filter(cdn_net_id=cdn_net_id, cdn_node_id=cdn_node_id,
                    cdn_house_id=cdn_house_id).delete()
            elif flag == "domain":
                MountCdnDomain.objects.filter(cdn_domain_id=cdn_domain_id).delete()     
            else:
                print("flag error!")
                pass

            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2

