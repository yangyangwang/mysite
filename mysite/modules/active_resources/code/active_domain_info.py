# coding=utf-8
from django.shortcuts import render_to_response


def active_domain_info(request):
  return render_to_response("active_domain_list.html", locals())


def block_domain_info(request):
  pass