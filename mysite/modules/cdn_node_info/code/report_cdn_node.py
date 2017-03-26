# coding=utf-8
from modules.share_part.share_func import get_cur_time, return_msg
from modules.dict_table.models import ReportStatus
from modules.business_unit.models import BusinessUnit
from modules.cdn_node_info.models import CdnNodeInfo
from config.config_parse import local_xml_path, local_xsd_path
from xml.dom.minidom import Document
from modules.share_part.handle_xml import *
import traceback
import json



# 更新上报cdn节点信息
def report_cdn_node(request):

    try:
        cdn_node_id = request.POST.get("cdn_node_id").strip()
        nodeName = CdnNodeInfo.objects.get(cdn_node_id=cdn_node_id).cdn_node_name
        report_status = CdnNodeInfo.objects.get(cdn_node_id=cdn_node_id).report_status

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
        xml_file = local_xml_path + "/basic_update_cdn_node_info.xml"
        xsd_file = local_xsd_path + "/basic_update_cdn_node_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence

        node = xml_obj.create_child_node(doc, NodeInfo, 'node')
        xml_obj.add_value_to_node(doc, node, 'nodeId', cdn_node_id)
        xml_obj.add_value_to_node(doc, node, 'nodeName', nodeName)

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
        return_code = ftp_report_cdn_node(report_status, xml_file, cdn_node_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_report_cdn_node(report_status, xml_file, cdn_node_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            tmp_status = "4"
            report_time = get_cur_time()
            CdnNodeInfo.objects.filter(cdn_node_id=cdn_node_id).update(report_status=tmp_status, 
                report_time = report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2
