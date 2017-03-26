from django.db import models

# Create your models here.

class Command(models.Model):

    command_id = models.BigIntegerField(u"管理指令ID", blank=True, null=True)
    command_type = models.CharField(u"指令类型", max_length=1, blank=True, null=True)
    operate_type = models.CharField(u"操作类型", max_length=1, blank=True, null=True)
    effect_time = models.CharField(u"生效时间", max_length=20, blank=True, null=True)
    deadline = models.CharField(u"过期时间", max_length=20, blank=True, null=True)
    unit_licence = models.CharField(u"经营者编号", max_length=20, blank=True, null=True)
    house = models.CharField(u"所属机房", max_length=30, blank=True, null=True)
    send_user = models.CharField(u"下发指令用户名", max_length=30, blank=True, null=True)
    command_origin = models.CharField(u"指令来源", max_length=20, blank=True, null=True)
    priority = models.CharField(u"优先级", max_length=20, blank=True, null=True)
    is_write_log = models.CharField(u"是否记录日志", max_length=5, blank=True, null=True)
    is_report = models.CharField(u"是否进行上传", max_length=5, blank=True, null=True)
    filter_reason = models.CharField(u"过滤原因", max_length=500, blank=True, null=True)
    rule_type = models.CharField(u"规则类型", max_length=1, blank=True, null=True)
    rule_start_value = models.CharField(u"规则内容起始值", max_length=50, blank=True, null=True)
    rule_end_value = models.CharField(u"规则内容结束值", max_length=50, blank=True, null=True)
    # 关键词匹配范围 1:正文标题及正文本身, 2:附件标题, 3:附件正文
    keyword = models.CharField(u"关键词匹配范围", max_length=20, blank=True, null=True)
    create_time = models.CharField(u"创建时间", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = u"管理指令"
