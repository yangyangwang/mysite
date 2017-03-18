from django.db import models


# Create your models here.
class BusinessUnit(models.Model):
    INDEXENTRY = (
        ('1', u'新增未上报'),
        ('2', u'新增已上报'),
        ('3', u'更新未上报'),
        ('4', u'更新已上报'),
    )

    unit_licence = models.CharField(u"IDC/ISP许可证", max_length=50, blank=True, null=True)
    unit_name = models.CharField(u"单位名称", max_length=30, blank=True, null=True)
    unit_addr = models.CharField(u"单位地址", max_length=60, blank=True, null=True)
    unit_zipcode = models.CharField(u"单位邮编", max_length=10, blank=True, null=True)
    unit_faren = models.CharField(u"企业法人", max_length=20, blank=True, null=True)
    netinfo_people = models.PositiveIntegerField(u"网络安全负责人", blank=True, null=True)
    emergency_people = models.PositiveIntegerField(u"应急联系人", blank=True, null=True)
    status = models.CharField(u"上报状态", max_length=1, blank=True, null=True, choices=INDEXENTRY)
    time = models.CharField(u"上报时间", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = u"经营者单位信息"
