from django.db import models


# Create your models here.
class CustomerInfo(models.Model):

    customer_id = models.CharField(u"客户编号", max_length=30, blank=True, null=True)
    unit_name = models.CharField(u"单位名称", max_length=30, blank=True, null=True)
    unit_address = models.CharField(u"单位地址", max_length=50, blank=True, null=True)
    unit_zipcode = models.CharField(u"单位邮编", max_length=10, blank=True, null=True)
    unit_nature = models.CharField(u"单位属性", max_length=20, blank=True, null=True)
    id_type = models.CharField(u"证件类型", max_length=10, blank=True, null=True)
    id_no = models.CharField(u"证件号码", max_length=30, blank=True, null=True)
    network_people = models.PositiveIntegerField(u"网络信息安全负责", blank=True, null=True)
    register_time = models.CharField(u"注册时间", max_length=20, blank=True, null=True)
    business_unit = models.PositiveIntegerField(u"所属经营者单位", blank=True, null=True)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = u"客户信息"


class AppServiceInfo(models.Model):
    service_id = models.CharField(u"服务编号", max_length=30, blank=True, null=True)
    service_content = models.CharField(u"服务内容", max_length=100, blank=True, null=True)
    customer_id = models.ForeignKey(CustomerInfo)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = u"应用服务信息"


class DomainInfo(models.Model):
    domain_id = models.CharField(u"域名编号", max_length=16)
    domain = models.CharField(u"域名", max_length=20)
    source_address = models.CharField(u"源站地址", max_length=30)
    record_num = models.CharField(u"备案号或许可证号", max_length=30)
    top_domain = models.CharField(u"顶级域名", max_length=20)
    app_service_id = models.ForeignKey(AppServiceInfo)
    report_status = models.CharField(u"上报状态", max_length=1, blank=True, null=True)
    report_time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)

    
    class Meta:
        verbose_name = u"域名信息"