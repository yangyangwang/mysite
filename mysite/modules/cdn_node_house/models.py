from django.db import models

# Create your models here.

# CDN节点机房
class CdnNodeHouse(models.Model):

	cdn_house_id = models.CharField(u"机房编号", max_length=16, blank=True, null=True)
	cdn_house_name = models.CharField(u"机房名称", max_length=30, blank=True, null=True)
	cdn_house_nature = models.CharField(u"机房属性", max_length=10, blank=True, null=True)
	business_unit = models.PositiveIntegerField(u"所属经营者单位", blank=True, null=True)
	house_province = models.CharField(u"机房所在省", max_length=20, blank=True, null=True)
	house_city = models.CharField(u"机房所在市", max_length=20, blank=True, null=True)
	house_county = models.CharField(u"机房所在县", max_length=20, blank=True, null=True)
	house_address = models.CharField(u"机房地址", max_length=40, blank=True, null=True)
	house_zipcode = models.CharField(u"机房邮编", max_length=10, blank=True, null=True)
	network_people = models.PositiveIntegerField(u"网络负责人", blank=True, null=True)
	report_status = models.CharField(u"状态", max_length=20, blank=True, null=True)
	report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)
	
	class Meta:
		verbose_name = u"CDN节点机房信息"


# CDN节点机房链路信息
class HouseLink(models.Model):

	house_id = models.ForeignKey(CdnNodeHouse)  
	gateway_ip = models.CharField(u"网关IP地址", max_length=10, blank=True, null=True)
	link_bandwidth = models.PositiveIntegerField(u"链路带宽", blank=True, null=True)
	link_type = models.CharField(u"链路类型", max_length=10, blank=True, null=True)
	link_access_unit = models.CharField(u"接入单位", max_length=30, blank=True, null=True)
	link_time = models.CharField(u"链路分配时间", max_length=20, blank=True, null=True)
	
	class Meta:
		verbose_name = u"CDN节点机房链路信息"


# CDN节点机房机架信息
class HouseFrame(models.Model):

	house_id = models.ForeignKey(CdnNodeHouse)  
	use_type = models.CharField(u"使用类型", max_length=1, blank=True, null=True)
	frame_name = models.CharField(u"机架/机位名称", max_length=30, blank=True, null=True)
	
	class Meta:
		verbose_name = u"CDN节点机房机架信息"


# CDN节点机房IP地址段信息
class HouseIpseg(models.Model):

	house_id = models.ForeignKey(CdnNodeHouse)  
	start_ip = models.CharField(u"起始IP", max_length=10, blank=True, null=True)
	end_ip = models.CharField(u"终止IP", max_length=10, blank=True, null=True)
	ip_use_type = models.CharField(u"IP地址使用方式", max_length=10, blank=True, null=True)
	
	class Meta:
		verbose_name = u"CDN节点机房IP地址段信息"