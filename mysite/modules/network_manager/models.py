from django.db import models


# Create your models here.
class NetworkManager(models.Model):
    ID_TYPE = (
        ('1', u'工商营业执照号码'),
        ('2', u'身份证'),
        ('3', u'组织机构代码证书'),
        ('4', u'事业法人证书'),
        ('5', u'军队代号'),
        ('6', u'社团法人证书'),
        ('7', u'护照'),
        ('8', u'军官证'),
        ('7', u'台胞证'),
        ('999', u'其他')
    )

    name = models.CharField(u"姓名", max_length=30)
    id_type = models.CharField(u"证件类型", max_length=3, choices=ID_TYPE)
    id_number = models.CharField(u"证件号码", max_length=20)
    tel = models.CharField(u"固定电话", max_length=20)
    phone = models.CharField(u"移动电话", max_length=20)
    email = models.CharField(u"email地址", max_length=20)

    class Meta:
        verbose_name = u"网络安全责任人"
