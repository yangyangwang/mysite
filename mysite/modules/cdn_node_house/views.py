from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..business_unit.models import BusinessUnit
from ..network_manager.models import NetworkManager
from ..share_part.share_func import *
from .models import CdnNodeHouse, HouseLink, HouseFrame, HouseIpseg
from ..dict_table.models import HouseNature, IpUseType, FrameUseType, LinkType, ReportStatus
import traceback
import json

# Create your views here.

# CDN节点机房信息
def cdn_node_house_list(request):
	try:
		ret_list = CdnNodeHouse.objects.all()
		if ret_list:
			for one in ret_list:
				# 机房属性
				one.cdn_house_nature = get_dict_name(one.cdn_house_nature, HouseNature)

				# 获取该机房的链路信息个数
				one.link_info = get_link_num(one.id)

				# 获取该机房的机架信息个数
				one.frame_info = get_frame_num(one.id)

				# 获取该机房的IP地址段信息个数
				one.ipseg_info = get_ipseg_num(one.id)

				one.network_people = get_name_byid_table(int(one.network_people), NetworkManager).name

				one.business_unit = get_name_byid_table(int(one.business_unit), BusinessUnit).unit_name

				one.report_status = get_dict_name(one.report_status, ReportStatus)
	except:
		print(traceback.print_exc())
	return render_to_response("cdn_node_house_list.html", locals())


# 添加编辑CDN节点机房信息
def add_cdn_node_house(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}
	
	def _get():
		# 机房属性下拉
		house_nature_select = get_table_data(HouseNature)

		# 网络负责人下拉
		network_people_select = get_table_data(NetworkManager)

		# 所属经营者单位下拉
		business_unit_select = get_table_data(BusinessUnit)


		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = CdnNodeHouse.objects.get(id = tmp_id)
			edit_map.cdn_house_nature_name = get_dict_name(edit_map.cdn_house_nature, HouseNature)
			edit_map.network_people_name = get_name_byid_table(edit_map.network_people, NetworkManager).name
			edit_map.business_unit_name = get_name_byid_table(edit_map.business_unit, BusinessUnit).unit_name

			# 从下拉框中过滤掉要编辑的数据
			house_nature_select = del_dict_one_item(edit_map.cdn_house_nature, house_nature_select)
			network_people_select = del_table_one_item(edit_map.network_people, network_people_select)
			business_unit_select = del_table_one_item(edit_map.business_unit, business_unit_select)

		return render_to_response('cdn_node_house_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")
        
	tmp_id = request.POST.get('id')
	cdn_house_id = request.POST.get('cdn_house_id')
	cdn_house_name = request.POST.get('cdn_house_name')
	cdn_house_nature = request.POST.get('cdn_house_nature')
	business_unit = request.POST.get('business_unit')
	house_province = request.POST.get('house_province')
	house_city = request.POST.get('house_city')
	house_county = request.POST.get('house_county')
	house_zipcode = request.POST.get('house_zipcode')
	network_people = request.POST.get('network_people')
	house_address = request.POST.get('house_address')
	report_time = '--'
	report_status = '1'


	def _update():
		try:
			# 如果上报状态为新增已上报，更新未上报，更新已上报修改时都变为更新未上报
			# 如果为新增未上报，不用修改
			report_status = get_report_status(tmp_id, CdnNodeHouse)
			if report_status in ["2", "3", "4"]:
				report_status = "3" 
			CdnNodeHouse.objects.filter(id=tmp_id).update(
	            cdn_house_name = cdn_house_name,
	            cdn_house_nature = cdn_house_nature,
	            business_unit = int(business_unit),
	            house_province = house_province,
	            house_city = house_city,
	            house_county = house_county,
	            house_zipcode = house_zipcode,
	            network_people = int(network_people),
	            house_address = house_address,
	            report_status = report_status
		    )
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		return HttpResponseRedirect('/cdn_node_house_list') 

	def _add():
	    try:
	        CdnNodeHouse.objects.create(
	            cdn_house_id = get_auto_16_id(),
	            cdn_house_name = cdn_house_name,
	            cdn_house_nature = cdn_house_nature,
	            business_unit = int(business_unit),
	            house_province = house_province,
	            house_city = house_city,
	            house_county = house_county,
	            house_zipcode = house_zipcode,
	            network_people = int(network_people),
	            house_address = house_address,
	            report_status = report_status,
	            report_time = report_time
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))
	    return HttpResponseRedirect('/cdn_node_house_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


# 删除cdn节点机房信息
def del_cdn_node_house(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}

	tmp_id = request.POST.get('id')

	# 后续添加的业务逻辑
	# 如果子网信息要删除，也要将子网下挂载的都进行删除

	try:
	    CdnNodeHouse.objects.filter(id=tmp_id).delete()
	except:
	    return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))


# 获取机房下链路的个数
def get_link_num(tmp_id=None):
	return HouseLink.objects.filter(house_id_id = tmp_id).count()


# 获取机房下机架的个数
def get_frame_num(tmp_id=None):
	return HouseFrame.objects.filter(house_id_id = tmp_id).count()


# 获取机房下IP地址段的个数
def get_ipseg_num(tmp_id=None):
	return HouseIpseg.objects.filter(house_id_id = tmp_id).count()


# 机房链路信息列表
def house_link_list(request):
	try:
		# 这里的house_id是为了找到对应的机房下的链路信息
		house_id = request.GET.get("id")

		if not house_id:
			# 当添加保存后，会重定向导致house_id丢失。此时从session中获取
			house_id = request.session.get("house_id")

		ret_list = HouseLink.objects.filter(house_id_id=house_id)
		if ret_list:
			for one in ret_list:
				one.link_type = get_dict_name(one.link_type, LinkType)
	except:
		print(traceback.print_exc())
	return render_to_response("house_link_list.html", locals())


# 添加机房链路信息
def add_house_link(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}

	def _get():
		link_type_select = get_table_data(LinkType)
		house_id = request.GET.get("house_id")

		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = HouseLink.objects.get(id = tmp_id)
			edit_map.link_type_name = get_dict_name(edit_map.link_type, LinkType)

			link_type_select = del_dict_one_item(edit_map.link_type, link_type_select)
			
		return render_to_response('house_link_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")

	# 链路对应的机房id
	house_id_tmp = request.POST.get('house_id') 	
	tmp_id = request.POST.get('id')
	gateway_ip = request.POST.get('gateway_ip')
	link_bandwidth = request.POST.get('link_bandwidth')
	link_type = request.POST.get('link_type')
	link_access_unit = request.POST.get('link_access_unit')
	link_time = request.POST.get('link_time')

	def _update():
		try:
			HouseLink.objects.filter(id=tmp_id).update(
		        gateway_ip = gateway_ip,
	            link_bandwidth = link_bandwidth,
	            link_type = link_type,
	            link_access_unit = link_access_unit,
	            link_time = link_time
		    )
			# 更新机房的上报状态
			house_id_id = HouseLink.objects.get(id=tmp_id).house_id_id
			cdn_house_id = CdnNodeHouse.objects.get(id=house_id_id).cdn_house_id
			house_status = CdnNodeHouse.objects.get(cdn_house_id=cdn_house_id).report_status
			if int(house_status) in [2, 4]:
				CdnNodeHouse.objects.filter(cdn_house_id=cdn_house_id).update(report_status="3")
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		# 获取该机架的house_id
		request.session["house_id"] = HouseLink.objects.get(id=tmp_id).house_id_id
		return HttpResponseRedirect('/house_link_list') 

	def _add():
	    try:
	        HouseLink.objects.create(
	        	house_id_id = int(house_id_tmp),
	            gateway_ip = gateway_ip,
	            link_bandwidth = link_bandwidth,
	            link_type = link_type,
	            link_access_unit = link_access_unit,
	            link_time = link_time
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))
	    request.session["house_id"] = house_id_tmp
	    return HttpResponseRedirect('/house_link_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


# 删除机房链路信息
def del_house_link(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}
	tmp_id = request.POST.get("id")

	back_dict["house_id"] = HouseLink.objects.get(id=tmp_id).house_id_id
	back_dict_err["house_id"] = HouseLink.objects.get(id=tmp_id).house_id_id
	try:
	    HouseLink.objects.filter(id=int(tmp_id)).delete()
	except:
		print(traceback.print_exc())
		return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))


# 公用删除函数（可以封装为一个类，其它的删除去重写父类中的删除函数）
def del_func(obj=None, tmp_id=""):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}

	try:
	    obj.objects.filter(id=int(tmp_id)).delete()
	except:
		print(traceback.print_exc())
		return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))


# 获取机房机架列表信息
def house_frame_list(request):
	try:
		# 这里的house_id是为了找到对应的机房下的机架信息
		house_id = request.GET.get("id")

		if not house_id:
			# 当添加保存后，会重定向导致house_id丢失。此时从session中获取
			house_id = request.session.get("house_id")
		ret_list = HouseFrame.objects.filter(house_id_id=house_id)
		if ret_list:
			for one in ret_list:
				one.use_type = get_dict_name(one.use_type, FrameUseType)
	except:
		print(traceback.print_exc())
	return render_to_response("house_frame_list.html", locals())


# 添加机房机架信息
def add_house_frame(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}

	def _get():
		use_type_select = get_table_data(FrameUseType)
		house_id = request.GET.get("house_id")
		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = HouseFrame.objects.get(id = tmp_id)
			edit_map.use_type_name = get_dict_name(edit_map.use_type, FrameUseType)

			use_type_select = del_dict_one_item(edit_map.use_type, use_type_select)
		
		return render_to_response('house_frame_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")

	house_id_tmp = request.POST.get('house_id') 
	tmp_id = request.POST.get('id')
	use_type = request.POST.get('use_type')
	frame_name = request.POST.get('frame_name')

	def _update():
		try:
			HouseFrame.objects.filter(id=tmp_id).update(
		        use_type = use_type,
	            frame_name = frame_name
		    )
			# 更新机房的上报状态
			house_id_id = HouseFrame.objects.get(id=tmp_id).house_id_id
			cdn_house_id = CdnNodeHouse.objects.get(id=house_id_id).cdn_house_id
			house_status = CdnNodeHouse.objects.get(cdn_house_id=cdn_house_id).report_status
			if int(house_status) in [2, 4]:
				CdnNodeHouse.objects.filter(cdn_house_id=cdn_house_id).update(report_status="3")
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		# 获取该机架的house_id
		request.session["house_id"] = HouseFrame.objects.get(id=tmp_id).house_id_id
		return HttpResponseRedirect('/house_frame_list') 

	def _add():
	    try:
	        HouseFrame.objects.create(
	        	house_id_id = house_id_tmp,
	            use_type = use_type,
	            frame_name = frame_name
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))

	    # 为了添加house_id到重定向的页面    
	    request.session["house_id"] = house_id_tmp
	    return HttpResponseRedirect('/house_frame_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


# 删除机房机架信息
def del_house_frame(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}
	tmp_id = request.POST.get("id")

	back_dict["house_id"] = HouseFrame.objects.get(id=tmp_id).house_id_id
	back_dict_err["house_id"] = HouseFrame.objects.get(id=tmp_id).house_id_id
	try:
		# 删除机房信息时，将机房下的机架，链路，IP地址段都删除掉
		LinkType.objects.filter(house_id_id=int(tmp_id)).delete()
		HouseFrame.objects.filter(house_id_id=int(tmp_id)).delete()
		IpUseType.objects.filter(house_id_id=int(tmp_id)).delete()

		HouseFrame.objects.filter(id=int(tmp_id)).delete()
	except:
		print(traceback.print_exc())
		return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))


# 机房IP地址段信息列表
def house_ipseg_list(request):
	try:
		# 这里的house_id是为了找到对应的机房下的IP地址段信息
		house_id = request.GET.get("id")

		if not house_id:
			# 当添加保存后，会重定向导致house_id丢失。此时从session中获取
			house_id = request.session.get("house_id")
		ret_list = HouseIpseg.objects.filter(house_id_id=house_id)
		if ret_list:
			for one in ret_list:
				one.ip_use_type = get_dict_name(one.ip_use_type, IpUseType)
	except:
		print(traceback.print_exc())
	return render_to_response("house_ipseg_list.html", locals())


# 添加机房IP地址段信息
def add_house_ipseg(request):
	back_dict = {"code": 0, "msg": "success"}
	back_dict_err = {"code": 1, "msg": "error"}

	def _get():
		house_id = request.GET.get("house_id")
		ip_use_type_select = get_table_data(IpUseType)
		if request.GET.get("id"):
			tmp_id = request.GET.get("id")
			edit_map = HouseIpseg.objects.get(id = tmp_id)
			edit_map.ip_use_type_name = get_dict_name(edit_map.ip_use_type, IpUseType)

			ip_use_type_select = del_dict_one_item(edit_map.ip_use_type, ip_use_type_select)
			
		return render_to_response('house_ipseg_edit.html', locals())

	if request.method == "GET":
		return _get()

	print("===================================")
	print(request.POST)
	print("===================================")

	house_id_tmp = request.POST.get('house_id')
	tmp_id = request.POST.get('id')
	start_ip = request.POST.get('start_ip')
	end_ip = request.POST.get('end_ip')
	ip_use_type = request.POST.get('ip_use_type')

	def _update():
		try:
			HouseIpseg.objects.filter(id=tmp_id).update(
		        start_ip = start_ip,
	            end_ip = end_ip,
	            ip_use_type = ip_use_type
		    )
			# 更新机房的上报状态
			house_id_id = HouseIpseg.objects.get(id=tmp_id).house_id_id
			cdn_house_id = CdnNodeHouse.objects.get(id=house_id_id).cdn_house_id
			house_status = CdnNodeHouse.objects.get(cdn_house_id=cdn_house_id).report_status
			if int(house_status) in [2, 4]:
				CdnNodeHouse.objects.filter(cdn_house_id=cdn_house_id).update(report_status="3")
		except:
		    print(traceback.print_exc())
		    return HttpResponse(json.dumps(back_dict_err))
		# 获取该机架的house_id
		request.session["house_id"] = HouseIpseg.objects.get(id=tmp_id).house_id_id
		return HttpResponseRedirect('/house_ipseg_list') 

	def _add():
	    try:
	        HouseIpseg.objects.create(
	        	house_id_id = house_id_tmp,
	            start_ip = start_ip,
	            end_ip = end_ip,
	            ip_use_type = ip_use_type
	        )
	    except:
	        print(traceback.print_exc())
	        return HttpResponse(json.dumps(back_dict_err))
	    request.session["house_id"] = house_id_tmp
	    return HttpResponseRedirect('/house_ipseg_list') 

	if request.method == "POST" and request.POST['id']:
	    return _update()
	return _add()


# 删除机房IP地址段信息
def del_house_ipseg(request):
	back_dict = {"code": "0", "msg": "success"}
	back_dict_err = {"code": "1", "msg": "error"}
	tmp_id = request.POST.get("id")

	back_dict["house_id"] = HouseIpseg.objects.get(id=tmp_id).house_id_id
	back_dict_err["house_id"] = HouseIpseg.objects.get(id=tmp_id).house_id_id
	try:
	    HouseIpseg.objects.filter(id=int(tmp_id)).delete()
	except:
		print(traceback.print_exc())
		return HttpResponse(json.dumps(back_dict_err))
	return HttpResponse(json.dumps(back_dict))