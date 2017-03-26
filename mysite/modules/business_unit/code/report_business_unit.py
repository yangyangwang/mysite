# coding = utf-8

import traceback
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import BusinessUnit
from modules.share_part.share_func import return_msg, get_cur_time
from modules.share_part.handle_xml import *
from modules.network_manager.models import NetworkManager
from xml.dom.minidom import Document
from modules.cdn_net_info.models import CdnNetInfo
from modules.customer_info.models import *
import time
import json
from config.config_parse import local_xml_path, local_xsd_path


# 上报经营者单位信息
def report_business_unit(request):

    try:
        tmp_id = request.POST.get("id")
        business_unit = BusinessUnit.objects.filter(id=tmp_id)[0]
        cdnId = business_unit.unit_licence
        cdnName = business_unit.unit_name
        cdnAdd = business_unit.unit_addr
        corp = business_unit.unit_faren
        report_status = business_unit.status
        netinfo_people = business_unit.netinfo_people

        # 网络安全责任人
        linkOfficerInfo = NetworkManager.objects.filter(id=netinfo_people)[0]

        name = linkOfficerInfo.name
        idType = linkOfficerInfo.id_type
        credentialsId = linkOfficerInfo.id_number
        tel = linkOfficerInfo.tel
        mobile = linkOfficerInfo.phone

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        if int(report_status) == 1:  # 新增未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'newInfo')
            xml_file = local_xml_path + "/basic_add_business_unit.xml"
            xsd_file = local_xsd_path + "/basic_add_business_unit.xsd"
        elif int(report_status) == 3:  # 更新未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
            xml_file = local_xml_path + "/basic_update_business_unit.xml"
            xsd_file = local_xsd_path + "/basic_update_business_unit.xsd"

        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnId', cdnId)
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnName', cdnName)
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnAdd', cdnAdd)
        xml_obj.add_value_to_node(doc, NodeInfo, 'corp', corp)

        linkOfficerInfo = xml_obj.create_child_node(doc, NodeInfo, 'linkOfficerInfo')
        xml_obj.add_value_to_node(doc, linkOfficerInfo, 'name', name)
        xml_obj.add_value_to_node(doc, linkOfficerInfo, 'idType', idType)
        xml_obj.add_value_to_node(doc, linkOfficerInfo, 'credentialsId', credentialsId)
        xml_obj.add_value_to_node(doc, linkOfficerInfo, 'tel', tel)
        xml_obj.add_value_to_node(doc, linkOfficerInfo, 'mobile', mobile)

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
        return_code = ftp_report_business_unit(report_status, xml_file, tmp_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_report_business_unit(report_status, xml_file, tmp_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            tmp_status = "2" if int(report_status) == 1 else "4"
            report_time = get_cur_time()
            BusinessUnit.objects.filter(id=tmp_id).update(status=tmp_status, time=report_time)
            return 0
        except:
            return 3
    else:
        return 2


# 注销经营者单位信息
def logout_business_unit(request):
    try:
        tmp_id = request.POST.get("id")
        cdnId = BusinessUnit.objects.get(id=tmp_id).unit_licence

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')

        deleteInfo = xml_obj.create_child_node(doc, basicInfo, 'deleteInfo')
        xml_file = local_xml_path + "/basic_delete_business_unit.xml"
        xsd_file = local_xsd_path + "/basic_delete_business_unit.xsd"

        xml_obj.add_value_to_node(doc, deleteInfo, 'cdnId', cdnId)
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
        return_code = ftp_logout_business_unit(xml_file, tmp_id)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_logout_business_unit(xml_file, tmp_id):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            report_time = get_cur_time()
            BusinessUnit.objects.filter(id=tmp_id).update(status="5", time=report_time)

            # 暂时先别删除，应该过几天之后删除。以防管局没有注销成功
            # 子网和客户信息都进行删除
            business_unit = BusinessUnit.objects.get(id=tmp_id)
            customer_info = CustomerInfo.objects.filter(business_unit=business_unit.id)
            for one in customer_info:
                app_service_info = AppServiceInfo.objects.filter(customer_id_id=one.id)
                for app in app_service_info:
                    # 删除域名信息
                    DomainInfo.objects.filter(app_service_id_id=app.id).delete()
                # 删除服务信息
                AppServiceInfo.objects.filter(customer_id_id=one.id).delete()
            # 删除客户信息
            CustomerInfo.objects.filter(business_unit=business_unit.id).delete()
            # 删除子网信息
            CdnNetInfo.objects.filter().delete()
            # 删除经营者单位信息
            BusinessUnit.objects.filter(id=tmp_id).delete()
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2
