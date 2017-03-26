# coding=utf-8
from django.shortcuts import render_to_response


def access_log_list(request):
  return render_to_response("access_log_list.html", locals())
