# coding=utf-8
from django.shortcuts import render_to_response


def illegal_website_list(request):
    
    return render_to_response("illegal_website_list.html", locals())
