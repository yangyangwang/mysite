# coding=utf-8
from django.shortcuts import render_to_response


def monitor_log_list(request):
  return render_to_response("monitor_log_list.html", locals())
