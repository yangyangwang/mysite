# coding=utf-8
from django.shortcuts import render_to_response


def active_ip_info(request):
  return render_to_response("active_ip_list.html", locals())


def block_ip_info(request):
  pass