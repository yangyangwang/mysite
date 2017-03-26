# coding=utf-8
from django.shortcuts import render_to_response


def suspected_exception_domain_list(request):
    return render_to_response("se_domain_list.html", locals())