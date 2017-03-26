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


# 上报客户信息
def report_customer_info(request):

    try:
        tmp_id = request.POST.get("id")
        customer_info = CustomerInfo.objects.filter(id=tmp_id)[0]

        customerId = customer_info.customer_id
        unitName = customer_info.unit_name
        unitNature = customer_info.unit_nature
        idType = customer_info.id_type
        idNumber = customer_info.id_no
        Add = customer_info.unit_address
        report_status = customer_info.report_status

        # 应用服务信息
        service_info = AppServiceInfo.objects.filter(customer_id_id=tmp_id)

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        if int(report_status) == 1:  # 新增未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'newInfo')
            xml_file = local_xml_path + "/basic_add_customer_info.xml"
            xsd_file = local_xsd_path + "/basic_add_customer_info.xsd"
        elif int(report_status) == 3:  # 更新未上报
            NodeInfo = xml_obj.create_child_node(doc, basicInfo, 'updateInfo')
            xml_file = local_xml_path + "/basic_update_customer_info.xml"
            xsd_file = local_xsd_path + "/basic_update_customer_info.xsd"

        # cdn许可证号
        cdnId = BusinessUnit.objects.all()[0].unit_licence
        xml_obj.add_value_to_node(doc, NodeInfo, 'cdnId', cdnId)

        customerInfo = xml_obj.create_child_node(doc, NodeInfo, 'customerInfo')

        xml_obj.add_value_to_node(doc, customerInfo, 'customerId', customerId)
        xml_obj.add_value_to_node(doc, customerInfo, 'unitName', unitName)
        xml_obj.add_value_to_node(doc, customerInfo, 'unitNature', unitNature)
        xml_obj.add_value_to_node(doc, customerInfo, 'idType', idType)
        xml_obj.add_value_to_node(doc, customerInfo, 'idNumber', idNumber)
        xml_obj.add_value_to_node(doc, customerInfo, 'Add', Add)

        # 当只有新增上报的时候，才报客户下的服务信息。如果客户的服务有变化，单独上报。
        # 更新上报只是针对客户自己的信息变化了。不包含服务
        if int(report_status) == 1:
            for one in service_info:
                serviceInfo = xml_obj.create_child_node(doc, customerInfo, 'serviceInfo')
                xml_obj.add_value_to_node(doc, serviceInfo, 'serviceId', one.service_id)
                for i in json.loads(one.service_content):
                    xml_obj.add_value_to_node(doc, serviceInfo, 'serviceContent', i)

                # 域名信息
                domain_info = DomainInfo.objects.filter(app_service_id_id=one.id)
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
            # 更新客户信息状态
            CustomerInfo.objects.filter(id=tmp_id).update(report_status=tmp_status, report_time=report_time)

            # 更新服务信息状态
            AppServiceInfo.objects.filter(customer_id_id=tmp_id).update(report_status=tmp_status, report_time=report_time)

            # 更新域名信息状态
            service_info = AppServiceInfo.objects.filter(customer_id_id=tmp_id)
            for one in service_info:
                DomainInfo.objects.filter(app_service_id_id=one.id).update(report_status=tmp_status, report_time=report_time)
            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2


# 注销客户信息
def logout_customer_info(request):
    try:
        tmp_id = request.POST.get("id")
        # flag 表示注销客户信息，服务信息，域名信息中的那一个
        flag = request.POST.get("flag")

        if flag == "customer":
            customer_info = CustomerInfo.objects.get(id=tmp_id)
            cdnId = BusinessUnit.objects.get(id=customer_info.business_unit).unit_licence
            xml_file = local_xml_path + "/basic_delete_customer_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_customer_info.xsd"
        elif flag == "service":
            app_service_info = AppServiceInfo.objects.get(id=tmp_id)
            customer_info = CustomerInfo.objects.get(id=app_service_info.customer_id_id)
            xml_file = local_xml_path + "/basic_delete_app_service_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_app_service_info.xsd"
        elif flag == "domain":
            domain_info = DomainInfo.objects.get(id=tmp_id)
            app_service_info = AppServiceInfo.objects.get(id=domain_info.app_service_id_id)
            customer_info = CustomerInfo.objects.get(id=app_service_info.customer_id_id)
            xml_file = local_xml_path + "/basic_delete_domain_info.xml"
            xsd_file = local_xsd_path + "/basic_delete_domain_info.xsd"
        else:
            return return_msg(4)  

        cdnId = BusinessUnit.objects.get(id=customer_info.business_unit).unit_licence

        doc = Document()
        xml_obj = XML()
        basicInfo = xml_obj.create_child_node(doc, doc, 'basicInfo')
        deleteInfo = xml_obj.create_child_node(doc, basicInfo, 'deleteInfo')
        xml_obj.add_value_to_node(doc, deleteInfo, 'cdnId', cdnId)

        customerDeleteList = xml_obj.create_child_node(doc, deleteInfo, 'customerDeleteList')
        xml_obj.add_value_to_node(doc, customerDeleteList, 'customerId', customer_info.customer_id)
        # 注销服务或域名信息
        if flag != "customer":
            serviceDeleteList = xml_obj.create_child_node(doc, customerDeleteList, 'serviceDeleteList')
            xml_obj.add_value_to_node(doc, serviceDeleteList, 'serviceId', app_service_info.service_id)
            # 注销域名信息
            if flag == "domain":
                xml_obj.add_value_to_node(doc, serviceDeleteList, 'domainId', domain_info.domain_id)
                for c in json.loads(app_service_info.service_content):
                    xml_obj.add_value_to_node(doc, serviceDeleteList, 'serviceContent', c)

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
        return_code = ftp_logout_customer_info(xml_file, tmp_id, flag)

        # 错误处理
        return return_msg(return_code)
    except:
        print(traceback.print_exc())
        return return_msg(4)


# xml上报FTP
def ftp_logout_customer_info(xml_file, tmp_id, flag):
    # 根据上报的类型获取上报文件的目录
    report_type = 7
    # ret = send_file_to_ftp(report_type, xml_file)
    ret = True

    # 上报成功后，更改数据的上报状态，失败后直接返回失败提示
    if ret is True:
        try:
            if flag == "customer":
                report_time = get_cur_time()
                CustomerInfo.objects.filter(id=tmp_id).update(report_status="5", report_time=report_time)

                # 删除客户对应的服务信息
                customer_info = CustomerInfo.objects.get(id=tmp_id)
                app_service_info = AppServiceInfo.objects.filter(customer_id_id=customer_info.id)
                for app in app_service_info:
                    # 删除域名信息
                    DomainInfo.objects.filter(app_service_id_id=app.id).delete()
                # 删除服务信息
                AppServiceInfo.objects.filter(customer_id_id=customer_info.id).delete()
                # 删除客户信息
                CustomerInfo.objects.filter(id=tmp_id).delete()
            elif flag == "service":
                app_service_info = AppServiceInfo.objects.get(id=tmp_id)
                DomainInfo.objects.filter(app_service_id_id=app_service_info.id).delete()
                AppServiceInfo.objects.filter(id=tmp_id).delete()
            else:
                DomainInfo.objects.filter(id=tmp_id).delete()

            return 0
        except:
            print(traceback.print_exc())
            return 3
    else:
        return 2
