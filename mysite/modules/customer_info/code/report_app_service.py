# coding = utf-8

import traceback
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import *
from modules.business_unit.models import BusinessUnit
from modules.share_part.share_func import return_msg, get_cur_time
from modules.share_part.handle_xml import *
from xml.dom.minidom import Document
from config.config_parse import local_xml_path, local_xsd_path
import time
import json


# 上报应用服务信息
def report_app_service(request):

    try:
        tmp_id = request.POST.get("id")


        app_service_info = AppServiceInfo.objects.filter(id=tmp_id)[0]
        report_status = app_service_info.report_status

        customer_info = CustomerInfo.objects.filter(id=app_service_info.customer_id_id)[0]
        customerId = customer_info.customer_id
        customer_report_status = customer_info.report_status

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        if int(report_status) == 1:  # 新增未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'newInfo')
            xml_file = local_xml_path + "/basic_add_app_service_info.xml"
            xsd_file = local_xsd_path + "/basic_add_app_service_info.xsd"
        elif int(report_status) == 3:  # 更新未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
            xml_file = local_xml_path + "/basic_update_app_service_info.xml"
            xsd_file = local_xsd_path + "/basic_update_app_service_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnId', cdnId)

        customerInfo = xml_obj.create_child_node(doc, NodeInfo, 'customerInfo')

        xml_obj.add_value_to_node(doc, customerInfo, 'customerId', customerId)

        # 判断客户信息是否已经上报过，如果没有上报添加上客户信息,防止客户信息没有上报，就去上报服务信息 
        if int(customer_report_status) == "1":
            xml_obj.add_value_to_node(doc, customerInfo, 'unitName', unitName)
            xml_obj.add_value_to_node(doc, customerInfo, 'unitNature', unitNature)
            xml_obj.add_value_to_node(doc, customerInfo, 'idType', idType)
            xml_obj.add_value_to_node(doc, customerInfo, 'idNumber', idNumber)
            xml_obj.add_value_to_node(doc, customerInfo, 'Add', Add)


        serviceInfo = xml_obj.create_child_node(doc, customerInfo, 'serviceInfo')
        xml_obj.add_value_to_node(doc, serviceInfo, 'serviceId', app_service_info.service_id)
        for i in json.loads(app_service_info.service_content):
            xml_obj.add_value_to_node(doc, serviceInfo, 'serviceContent', i)

        # 当只有新增上报的时候，才报服务下的域名信息。如果客户的域名有变化，单独上报。
        # 更新上报只是针对服务自己的信息变化了（服务内容）。不包含其它
        if int(report_status) == 1:
            # 域名信息
            domain_info = DomainInfo.objects.filter(app_service_id_id=app_service_info.id)
            for d in domain_info:
                domainInfo = xml_obj.create_child_node(doc, serviceInfo, 'domainInfo')
                xml_obj.add_value_to_node(doc, domainInfo, 'domainId', d.domain_id)
                xml_obj.add_value_to_node(doc, domainInfo, 'domain', d.domain)
                xml_obj.add_value_to_node(doc, domainInfo, 'regId', d.record_num)

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

            # 更新客户信息状态,如果客户是新增未上报时，其它不用更新
            customer_id_id = AppServiceInfo.objects.get(id=tmp_id).customer_id_id
            customer_report_status = CustomerInfo.objects.get(id=customer_id_id).report_status
            if int(customer_report_status) == 1:
                CustomerInfo.objects.filter(id=customer_id_id).update(report_status="2", report_time=report_time)

            # 更新服务信息状态
            AppServiceInfo.objects.filter(id=tmp_id).update(report_status=tmp_status, report_time=report_time)

            # 更新域名信息状态,当服务信息是新增上报的时候。
            if int(report_status) == 1:
                DomainInfo.objects.filter(app_service_id_id=tmp_id).update(report_status=tmp_status, report_time=report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2
