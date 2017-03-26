# coding=utf-8
from django.shortcuts import render_to_response


def suspected_exception_command_list(request):
    return render_to_response("se_command_list.html", locals())