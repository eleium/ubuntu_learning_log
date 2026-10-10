from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    #此时因为更改了模型，需要再次数据迁移：python manage.py makemigrations --> migrate 
    
    def __str__(self):
        return self.text
    #这个模型的核心作用就是返回自己的text属性。

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    #外键：ForeignKEey ,
    
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        #class Meta 是 Django 模型的“配置中心”，用来设置模型在数据库和 admin 后台中的行为，它不是数据本身，而是“关于数据的配置”。
           verbose_name_plural = "entries"
#         类别	            示例	                                    说明
#         显示名称	        verbose_name、verbose_name_plural	        在 admin 后台显示的名字
#         默认排序	        ordering = ['-date_added']	                查询时默认按什么排序
#         数据库表名	    db_table = 'my_entries'	                    指定数据库中的表名
#         唯一约束	        unique_together = [['topic', 'text']]	    组合字段唯一
#         权限	            permissions = [...]                     	自定义权限
#         抽象基类	        abstract = True	                            声明为抽象模型，不建表

    def __str__(self):
        return self.text
