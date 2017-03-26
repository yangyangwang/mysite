# coding=utf-8
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import random
import string
import json
import time

# 通过字典表key id 获取name值
def get_dict_name(tmp_id=None, obj=None):
    tmp_dict_list = get_table_data(obj)
    for one in tmp_dict_list:
        if int(one.key) == int(tmp_id):
            return one.value
    return None


# 过滤掉某一个字典表中的item
def del_dict_one_item(key=None, dict_list=None):

    tmp_list = dict_list
    filter_list = filter(lambda x: int(x.key) != int(key), tmp_list)
    ret_list = list(filter_list)
    return ret_list


# 过滤掉某一个数据表中的item
def del_table_one_item(tmp_id=None, dict_list=None):

    tmp_list = dict_list
    filter_list = filter(lambda x: int(x.id) != int(tmp_id), tmp_list)
    ret_list = list(filter_list)
    return ret_list


# 查询相应数据库表中的数据
def get_table_data(obj=None):
    TMPOBJECT = obj
    return TMPOBJECT.objects.all()


# 通过id获取相应的数据字段在数据库表中
def get_name_byid_table(tmp_id=None, obj=None):

    TMPOBJECT = obj
    tmp_map = TMPOBJECT.objects.get(id=tmp_id)
    return tmp_map if tmp_map else None


# 随机生成16UUID
def get_auto_16_id(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_cur_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


# 获取查询数据的上报状态
def get_report_status(tmp_id=None, obj=None):
    return obj.objects.filter(id=tmp_id).values("report_status")[0].get("report_status")


# 处理上报结果返回提示给页面
def return_msg(code=None):
    no_err = {"code": "0", "msg": u"上报成功！"}
    xsd_err = {"code": "1", "msg": u"xml文件xsd校验失败！"}
    ftp_err = {"code": "2", "msg": u"XML上报FTP失败！"}
    update_err = {"code": "3", "msg": u"XML上报成功，更新数据上报状态失败！"}
    exception_err = {"code": "4", "msg": u"组装XML数据异常！"}
    if code == 0:
        return HttpResponse(json.dumps(no_err))
    elif code == 1:
        return HttpResponse(json.dumps(xsd_err))
    elif code == 2:
        return HttpResponse(json.dumps(ftp_err))
    elif code == 3:
        return HttpResponse(json.dumps(update_err))
    elif code == 4:
        return HttpResponse(json.dumps(exception_err))





