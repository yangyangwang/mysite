# coding = utf-8
from django.shortcuts import render
from .models import *

# Create your views here.

# 单位属性
UnitNatureMap = {
	"1": u"军队",
	"2": u"政府机关",
	"3": u"事业单位",
	"4": u"企业",
	"5": u"个人",
	"6": u"社会团体",
	"999": u"其他"
}

# 证件类型
IdTypeMap = {
	"1": u"工商经营执照号码",
	"2": u"身份证",
	"3": u"组织机构代码证书",
	"4": u"事业法人证书",
	"5": u"军队代号",
	"6": u"社团法人证书",
	"7": u"护照",
	"8": u"军官证",
	"9": u"台胞证",
	"999": u"护照"
}

# 机房属性
HouseNatureMap = {
	"1": u"租用",
	"2": u"自建",
	"999": u"护照"
}

# IP使用方式
IpUseTypeMap = {
	"0": u"静态",
	"1": u"动态",
	"2": u"保留"
}

# 机架使用类型
FrameUseTypeMap = {
	"1": u"自用",
	"2": u"出租"
}

# 链路类型
LinkTypeMap = {
	"1": u"电信",
	"2": u"联通",
	"3": u"移动",
	"4": u"铁通",
	"9": u"其他"
}

# 上报状态
ReportStatusMap = {
	"1": u"新增未上报",
	"2": u"新增已上报",
	"3": u"更新未上报",
	"4": u"更新已上报"
}

# 服务内容
ServiceContentMap = [
	("500", "/", u"基础应用"),
	("501", "/", u"网络媒体"),
	("502", "/", u"电子政务、电子商务"),
	("503", "/", u"数字娱乐"),
	("504", "/", u"其他"),

	("1", "500", u"即时通信"),
	("2", "500", u"搜索引擎"),
	("3", "500", u"综合门户"),
	("4", "500", u"网上邮局"),
	("5", "501", u"网络新闻"),
	("6", "501", u"博客/个人空间"),
	("7", "501", u"网络广告/信息"),
	("8", "501", u"单位门户网站"),
	("9", "502", u"网络购物"),
	("10", "502", u"网上支付"),
	("11", "502", u"网上银行"),
	("12", "502", u"网上炒股/股票基金"),
	("13", "503", u"网络游戏"),
	("14", "503", u"网络音乐"),
	("15", "503", u"网络影视"),
	("16", "503", u"网络图片"),
	("17", "503", u"网络软件/下载"),
	("18", "504", u"网上求职"),
	("19", "504", u"网上交友/婚介"),
	("20", "504", u"网上房产"),
	("21", "504", u"网络教育"),
	("22", "504", u"网站建设"),
	("23", "504", u"WAP"),
	("24", "504", u"其他")
]


map_list = [
	(UnitNatureMap, UnitNature),
	(IdTypeMap, IdType),
	(HouseNatureMap, HouseNature),
	(IpUseTypeMap, IpUseType),
	(LinkTypeMap, LinkTypeMap),
	(ReportStatusMap, ReportStatusMap)
]


# 初始化字典表数据
def init_dict_table_content(tmp_dict, obj):
	print("---start init %s table---" % obj)
	for key, value in tmp_dict.items():
	    obj.objects.create(
	        key = key,
	        value = value
	    )
	print("---init %s complate---" % obj)


# 初始化特殊字典表，服务内容表
def init_service_content_table(tmp_list, obj):
	print("---start init %s table---" % obj)
	for one in tmp_list.items():
	    obj.objects.create(
	    	parent_id = one[1],
	        key = one[0],
	        value = one[-1]
	    )
	print("---init %s complate---" % obj)


if __name__ == '__main__':
	# 初始化其他字典表
	for one in map_list:
		init_dict_table_content(one[0], one[1])

	# 初始化服务内容字典表
	init_service_content_table(ServiceContentMap, ServiceContent)