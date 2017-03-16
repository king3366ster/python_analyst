# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Monitor(models.Model):
	# 监控名称
    monitor_name = models.CharField(
    	max_length = 128,
    	unique = True,
    	null = False,
    	verbose_name = u'监控名称',
    )
    # 执行脚本内容
    monitor_text = models.TextField(
    	default = '',
    	verbose_name = u'执行脚本',
    )
    monitor_month = models.CharField(
    	max_length = 32,
    	default='0',
    	verbose_name = u'定时月份',
    )
    monitor_day = models.CharField(
    	max_length = 32,
    	default='0',
    	verbose_name = u'定时日期',
    )
    monitor_hour = models.CharField(
    	max_length = 32,
    	default='0',
    	verbose_name = u'定时小时',
    )
    monitor_minute = models.CharField(
    	max_length = 32,
    	default='0',
    	verbose_name = u'定时分钟',
    )
    email_enable = models.BooleanField(
    	default=False,
    	verbose_name = u'开启邮件提醒',
    )
    email_to = models.TextField(
    	default='',
    	verbose_name = u'邮件对象',
    )
    email_subject = models.TextField(
    	default='',
    	verbose_name = u'邮件内容',
    )
    created_at = models.DateTimeField(
        auto_now_add = True,
        verbose_name = u'创建时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name = u'更新时间',
    )
    def __str__(self):
        return "%s" % (self.monitor_name, )
    def __unicode__(self):
        return u'%s' % (self.monitor_name, )
    class Meta:
        verbose_name = '后台监控配置'

class Privilege(models.Model):
    class Meta:
        permissions = (
            ('perm_public','Privilege for Public'),
            ('perm_seller','Privilege for Seller'),
            ('perm_operator','Privilege for Operator'),
            ('perm_productor','Privilege for Productor'),
        )
    permname = models.CharField(
        max_length = 128,
        unique = True,
        verbose_name = u'权限名称',
    )
    permission = models.CharField(
        max_length = 128,
        verbose_name = u'权限内容',
    )
    def __str__(self):
        return "%s" % (self.monitor_name, )
    def __unicode__(self):
        return u'%s' % (self.monitor_name, )
    class Meta:
        verbose_name = '权限配置'
