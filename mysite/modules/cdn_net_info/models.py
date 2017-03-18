from django.db import models

# Create your models here.

class CdnNetInfo(models.Model):

	cdn_net_id = models.CharField(u"cdn子网编号", max_length=16)
	cdn_top_domain = models.CharField(u"cdn子网顶级域名", max_length=20)
	top_domain_record_num = models.CharField(u"cdn子网顶级域名备案号", max_length=30)
	report_status = models.CharField(u"上报状态", max_length=1)
	report_time = models.CharField(u"上报时间", max_length=20)
	
	class Meta:
		verbose_name = u"CDN子网信息"

