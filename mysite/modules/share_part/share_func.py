# coding = utf-8
import random
import string

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


# 获取查询数据的上报状态
def get_report_status(tmp_id=None, obj=None):
    return obj.objects.filter(id=tmp_id).values("report_status")[0].get("report_status")


