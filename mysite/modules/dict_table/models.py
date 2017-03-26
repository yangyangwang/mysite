from django.db import models

# Create your models here.
class UnitNature(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"单位属性", max_length=30)

	class Meta:
	    verbose_name = u"单位属性"


class IdType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"证件类型", max_length=30)

	class Meta:
		verbose_name = u"证件类型"


class HouseNature(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"机房属性", max_length=30)

	class Meta:
	    verbose_name = u"机房属性"


class IpUseType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"IP使用方式", max_length=30)

	class Meta:
	    verbose_name = u"IP使用方式"


class FrameUseType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"机架使用类型", max_length=30)

	class Meta:
	    verbose_name = u"机架使用类型"


class LinkType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"链路类型", max_length=30)

	class Meta:
	    verbose_name = u"链路类型"


class ReportStatus(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"名称", max_length=30)

	class Meta:
	    verbose_name = u"上报状态"


class ServiceContent(models.Model):

	parent_id = models.CharField(u"父类", max_length=10)
	key = models.CharField(u"类型序号", max_length=10)
	value = models.CharField(u"服务内容名称", max_length=30)

	class Meta:
	    verbose_name = u"服务内容"


class CommandType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"名称", max_length=30)

	class Meta:
	    verbose_name = u"指令类型"


class CommandOperateType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"名称", max_length=30)

	class Meta:
	    verbose_name = u"指令操作类型"


class RuleType(models.Model):

	key = models.CharField(u"代码", max_length=10)
	value = models.CharField(u"名称", max_length=30)

	class Meta:
	    verbose_name = u"规则类型"