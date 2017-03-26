# coding=utf-8
from django.shortcuts import render_to_response


def basic_data_monitor(request):
    
    return render_to_response("basic_data_monitor_list.html", locals())
