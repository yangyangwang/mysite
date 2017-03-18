from django.db import models

# Create your models here.
class Userinfo(models.Model):
	name = models.CharField(max_length=30, verbose_name="名称")
	address = models.CharField("地址", max_length=50)
	city = models.CharField(max_length=60)
	
	class Meta:
		verbose_name= '用户信息'
