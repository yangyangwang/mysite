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
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_licence', models.CharField(blank=True, max_length=50, null=True, verbose_name='IDC/ISP许可证')),
                ('unit_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='单位名称')),
                ('unit_addr', models.CharField(blank=True, max_length=60, null=True, verbose_name='单位地址')),
                ('unit_zipcode', models.CharField(blank=True, max_length=10, null=True, verbose_name='单位邮编')),
                ('unit_faren', models.CharField(blank=True, max_length=20, null=True, verbose_name='企业法人')),
                ('netinfo_people', models.PositiveIntegerField(blank=True, null=True, verbose_name='网络安全负责人')),
                ('emergency_people', models.PositiveIntegerField(blank=True, null=True, verbose_name='应急联系人')),
                ('status', models.CharField(blank=True, choices=[('1', '新增未上报'), ('2', '新增已上报'), ('3', '更新未上报'), ('4', '更新已上报')], max_length=1, null=True, verbose_name='上报状态')),
                ('time', models.CharField(blank=True, max_length=20, null=True, verbose_name='上报时间')),
            ],
            options={
                'verbose_name': '经营者单位信息',
            },
        ),
    ]