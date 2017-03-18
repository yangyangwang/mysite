from django.db import models

# Create your models here.

class CdnNodeInfo(models.Model):

	cdn_node_id = models.CharField(u"cdn节点编号", max_length=16, blank=True, null=True)
	cdn_node_name = models.CharField(u"cdn节点名称", max_length=30, blank=True, null=True)
	report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
	report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)
	
	class Meta:
		verbose_name = u"CDN节点信息"