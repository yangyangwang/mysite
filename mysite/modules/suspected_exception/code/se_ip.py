# coding=utf-8
from django.shortcuts import render_to_response


def suspected_exception_ip_list(request):
    return render_to_response("se_ip_list.html", locals())