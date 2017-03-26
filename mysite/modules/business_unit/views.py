# coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..network_manager.models import NetworkManager
from django.views.decorators.csrf import csrf_exempt
from .models import BusinessUnit
from ..share_part.share_func import *
from ..share_part.handle_xml import *
from ..dict_table.models import IdType, ReportStatus
from django.core.paginator import Paginator
import json
import traceback


# Create your views here.


# # 经营者单位信息列表
# class BusinessUnitList(ListView):
#     context_object_name = "business_unit_list"
#     template_name = "business_unit_list.html"
#     allow_empty = True
#     paginate_by = 30
#     model = BusinessUnit

#     def get_queryset(self):
#         print("get_queryset")
#         ret_list = BusinessUnit.objects.all()
#         print(ret_list)
#         return ret_list

#     def get_context_data(self, **kwargs):
#         # kwargs['it_list'] = Category.objects.all().order_by('name')
#         #       return super(BusinessUnitList, self).get_context_data(**kwargs)

#         print("get_context_data")
#         context = super(BusinessUnitList, self).get_context_data(**kwargs)
#         # content 估计是填充查询条件
#         # context["unit_licence"] = self.unit_licence
#         print(context)
#         return context


# # 添加编辑经营者单位信息
# class BusinessUnitCreate(SuccessMessageMixin, CreateView):
#     template_name = "business_unit_edit.html"
#     model = BusinessUnit
#     success_message = u"%(unit_name)s 成功创建"
#     fields = [
#         "unit_licence",
#         "unit_name",
#         "unit_addr",
#         "unit_zipcode",
#         "unit_faren",
#         "netinfo_people",
#         "emergency_people"
#     ]

#     def get_success_url(self):
#         self.url = "/business_unit_list"
#         return self.url

#     # def get_context_data(self, **kwargs):
#     # 	context = super(BusinessUnitCreate, self).get_context_data(**kwargs)
#     # 	referrer = self.request.META.get('HTTP_REFERER', "")
#     # 	context["referrer"] = referrer
#     # 	return context


# class BusinessUnitCreate(SuccessMessageMixin, UpdateView):
#     template_name = "business_unit_edit.html"
#     model = BusinessUnit
#     success_message = u"%(name)s 成功修改"

#     def get_success_url(self):
#         self.url = "/business_unit_list"
#         return self.url



# 获取经营者单位信息列表
def business_unit_list(request):
    # 按单位名称查询
    if request.GET.get("unit_name"):
        unit_name = request.GET.get("unit_name")
        tmp_list = BusinessUnit.objects.filter(unit_name=unit_name.strip())
    else:
        tmp_list = BusinessUnit.objects.all()

    # 每页列表显示的数量，读配置文件获取
    PAGE_SIZE = 5
    page_size = PAGE_SIZE

    # 要获取的第几页数据，默认为第一页
    try:
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    # 创建分页对象
    paginator = Paginator(tmp_list, page_size)
    page_obj = paginator.page(page)

    for one in page_obj.object_list:
        one.emergency_people = get_name_byid_table(int(one.emergency_people), NetworkManager).name
        one.netinfo_people = get_name_byid_table(int(one.netinfo_people), NetworkManager).name
        one.status = get_dict_name(one.status, ReportStatus)

    return render_to_response('business_unit_list.html', locals())


# 添加编辑经营者单位信息
def add_business_unit(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "save error"}

    def _get():

        # 获取下拉框中的数据
        select_item_list = get_table_data(NetworkManager)
        print("###", select_item_list)

        if request.GET.get('id', None):  # 表示获取要编辑的数据
            edit_map = BusinessUnit.objects.filter(id = request.GET['id'])[0]

            edit_map.netinfo_people_name = get_name_byid_table(edit_map.netinfo_people, NetworkManager).name
            edit_map.emergency_people_name = get_name_byid_table(edit_map.emergency_people, NetworkManager).name

            # 过滤掉字典表列表中的选中项
            select_item_list = del_table_one_item(edit_map.emergency_people, select_item_list)

        return render_to_response('business_unit_edit.html', locals())

    if request.method == "GET":
        return _get()

    # 下面表示post请求
    print("===================================")
    print(request.POST)
    print("===================================")
    
    tmp_id = request.POST.get("id")
    unit_licence = request.POST.get('unit_licence')
    unit_name = request.POST.get('unit_name')
    unit_addr = request.POST.get('unit_addr')
    unit_zipcode = request.POST.get('unit_zipcode')
    unit_faren = request.POST.get('unit_faren')
    netinfo_people = request.POST.get('netinfo_people')
    emergency_people = request.POST.get('emergency_people')

    def _update():
        try:
            BusinessUnit.objects.filter(id=tmp_id).update(
                unit_licence = unit_licence,
                unit_name = unit_name,
                unit_addr = unit_addr,
                unit_zipcode = unit_zipcode,
                unit_faren = unit_faren,
                netinfo_people = netinfo_people,
                emergency_people = emergency_people,
                status = 3
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/business_unit_list') 

    def _add():
        try:
            BusinessUnit.objects.create(
                unit_licence = unit_licence,
                unit_name = unit_name,
                unit_addr = unit_addr,
                unit_zipcode = unit_zipcode,
                unit_faren = unit_faren,
                netinfo_people = netinfo_people,
                emergency_people = emergency_people,
                time = '',
                status = 1
            )
        except:
            print(traceback.print_exc())
            return HttpResponse(json.dumps(back_dict_err))
        return HttpResponseRedirect('/business_unit_list') 

    if request.method == "POST" and request.POST.get('id'):
        return _update()
    return _add()


# 删除经营者单位信息
def del_business_unit(request):
    back_dict = {"code": "0", "msg": "success"}
    back_dict_err = {"code": "1", "msg": "error"}

    tmp_id = request.POST.get('id')
    try:
        BusinessUnit.objects.filter(id=tmp_id).delete()
    except:
        return HttpResponse(json.dumps(back_dict_err))
    return HttpResponse(json.dumps(back_dict))

