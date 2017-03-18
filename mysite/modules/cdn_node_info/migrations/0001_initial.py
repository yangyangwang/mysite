# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CdnNodeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdn_node_id', models.CharField(blank=True, max_length=16, null=True, verbose_name='cdn节点编号')),
                ('cdn_node_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='cdn节点名称')),
                ('report_status', models.CharField(blank=True, max_length=1, null=True, verbose_name='上报状态')),
                ('report_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='上报时间')),
            ],
            options={
                'verbose_name': 'CDN节点信息',
            },
        ),
    ]