#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 公司信息蓝图，构建在：/stu

from flask import Blueprint,request,render_template,url_for
from flask_login import current_user
from stucrs.model import Session, session_scope

from stucrs.model import search_company_list, search_company_details_by_company_id
from .project_utils import dRet

companys = Blueprint('companys',__name__)

# 显示数据库表 RecruitmentCompany 中的记录
@companys.route('/list',methods=['GET','POST'])
def list():
	form_data = {
		'company_name': '',				# 公司名
		'company_industry': '',			# 行业
		'address': '',					# 公司地点
		'page': '',  					# 分页
		'pagesize': ''  				# 单页数量
	}
	# 查询post表单初始化字段
	if request.method=='POST':
		for k in form_data.keys():
			form_data[k] = request.form.get(k, '')

	# 分页的转换单独写
	try:
		form_data['page'] = int(form_data['page'])
		if form_data['page'] < 1:
			form_data['page'] = 1
	except:
		form_data['page'] = 1
	try:
		form_data['pagesize'] = int(form_data['pagesize'])
	except:
		form_data['pagesize'] = 20

	with session_scope() as session:
		# 查询数据
		companys_data = search_company_list(current_user, form_data)
		# import pprint
		# pprint.pprint(companys_data)
		return render_template('tcompany_list.html', companys_data=companys_data)

# 根据公司id显示公司详情页面
@companys.route('/details',methods=['GET'])
def details():
	company_id = int(request.args.get('id'))
	print("获取公司详情：", company_id)
	if company_id:
		with session_scope() as session:
			ret = search_company_details_by_company_id(company_id)
			return render_template('tcompany_detail.html', data=ret.get('data'))
	return None

