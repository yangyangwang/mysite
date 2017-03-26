from django.db import models

# Create your models here.

class CdnNetInfo(models.Model):

    cdn_net_id = models.CharField(u"cdn子网编号", max_length=16, blank=True, null=True)
    cdn_top_domain = models.CharField(u"cdn子网顶级域名", max_length=20, blank=True, null=True)
    top_domain_record_num = models.CharField(u"cdn子网顶级域名备案号", max_length=30, blank=True, null=True)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)
    create_time = models.CharField(u"创建时间", max_length=20, blank=True, null=True)
	
    class Meta:
    	verbose_name = u"CDN子网信息"


class MountCdnNode(models.Model):

    cdn_net_id = models.CharField(u"cdn子网编号", max_length=16, blank=True, null=True)
    cdn_node_id = models.CharField(u"cdn节点编号", max_length=16, blank=True, null=True)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)
    create_time = models.CharField(u"创建时间", max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = u"CDN节点挂载机房"


class MountCdnDomain(models.Model):

    cdn_net_id = models.CharField(u"cdn子网编号", max_length=16, blank=True, null=True)
    cdn_domain_id = models.CharField(u"cdn域名编号", max_length=16, blank=True, null=True)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)
    create_time = models.CharField(u"创建时间", max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = u"CDN子网挂载加速域名"

