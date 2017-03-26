# coding=utf-8
from modules.share_part.share_func import get_cur_time, return_msg
from modules.dict_table.models import ReportStatus
from modules.business_unit.models import BusinessUnit
from modules.cdn_node_info.models import CdnNodeInfo
from config.config_parse import local_xml_path, local_xsd_path
from modules.cdn_node_house.models import CdnNodeHouse, HouseLink, HouseFrame, HouseIpseg
from xml.dom.minidom import Document
from modules.share_part.handle_xml import *
import traceback
import json



# 更新上报cdn机房信息
def report_house_info(request):

    try:
        cdn_house_id = request.POST.get("cdn_house_id").strip()
        h = CdnNodeHouse.objects.get(cdn_house_id=cdn_house_id)

        report_status = h.report_status

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
        xml_file = local_xml_path + "/basic_update_cdn_house_info.xml"
        xsd_file = local_xsd_path + "/basic_update_cdn_house_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence
        cdnName = BusinessUnit.objects.all()[0].unit_name

        houseInfo = xml_obj.create_child_node(doc, NodeInfo, 'houseInfo')

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
        return_code = ftp_report_cdn_house(report_status, xml_file, cdn_house_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_report_cdn_house(report_status, xml_file, cdn_house_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            tmp_status = "4"
            report_time = get_cur_time()
            CdnNodeHouse.objects.filter(cdn_house_id=cdn_house_id).update(report_status=tmp_status, 
                report_time = report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2
