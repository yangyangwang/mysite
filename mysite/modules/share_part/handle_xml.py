# coding = utf-8

from xml.dom import minidom
# from lxml import etree
import time
import random


class XML(object):
    def __init__(self):
        pass

    # 创建xml子节点
    def create_child_node(self, doc, parent, node):
        # doc 为XML创建的Document对象
        # parent 为父节点
        # 返回生成的节点
        tmp_node = doc.createElement(node)
        parent.appendChild(tmp_node)

        return tmp_node

    # 创建节点并且给节点赋值
    def add_value_to_node(self, doc, parent, name, value):
        tmp_node = self.create_child_node(doc, parent, name)

        tmp_value = doc.createTextNode(value)
        tmp_node.appendChild(tmp_value)

    def get_node_xml(self, parent, node_name):
        try:
            node = parent.getElementsByTagName(node_name)
        except:
            node_str = ''
        else:
            try:
                node_str = node[0].childNodes[0].nodeValue
            except:
                node_str = ''

        return node_str

    def parse_return_xml(self, filename):
        dom = minidom.parse(filename)
        root = dom.documentElement
        code = self.get_node_xml(root, "resultCode")

        return code


# 校验xml文件是否有误
def check_xml_file(xsd_file, xml_file):
    pass
    return 1

    # print("check xml %s！" % xml_file)
    # xmlschema_doc = etree.parse(xsd_file)
    # xmlschema = etree.XMLSchema(xmlschema_doc)
    # doc = etree.parse(xml_file)
    # print(xmlschema.error_log)
    # if xmlschema.validate(doc) is True:
    #     print("Success!!")
    #     return 1
    # else:
    #     return 0


# 获取管局FTP文件的存放目录
def get_report_ftp_path(type_tmp=7):
    pathname = '/' + str(type_tmp) + '/' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    pathname = pathname + '/' + str(int(time.time() * 1000)) + str(random.randint(1000, 9999)) + ".xml"

    return pathname


# 上传xml文件到FTP
def send_file_to_ftp(report_type, xml_file):
    # 获取管局FTP存放文件的目录
    # report_type代表不同的文件的路径标号
    remote = get_report_ftp_path(report_type)
    if not remote:
        print(u"获取管局FTP上报目录失败！")
        return None
    xml = xml_file, remote

    # 获得ftp参数
    ftp = ftp_arg()
    UP = upload()

    # 调用file_load方法上传文件
    res = UP.file_load(idcId, xml, ftp)

    if not res:
        return None
    result = res.split('-', 2)[2]
    if int(result) == 0:
        print
        "Upload xml file success!!!"
        return 1
    else:
        print
        "Upload xml file failed!!!"
        return 0