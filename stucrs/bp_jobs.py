#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图，职位列表模块，/jobs

from flask import Blueprint,request,render_template,url_for
from flask_login import login_user,logout_user,login_required,current_user

from stucrs.model import search_job_list, delivery_by_job_id
from .project_utils import get_db_path, datestr_to_timestamp, to_json, dRet

jobs = Blueprint('jobs',__name__)

# 显示数据库表 RecruitmentPosition 中的记录
@jobs.route('/list',methods=['GET','POST'])
def list():
	form_data = {
		'start_time': '',				# 发布时间 YYYY-MM-DD
		'end_time': '',					# 发布时间 YYYY-MM-DD
		'education_requirements': '',	# 学历要求
		'company_industry': '',			# 所属行业
		'work_city': '',				# 城市
		'page': '',						# 分页
		'pagesize': ''					# 单页数量
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
		form_data['pagesize']=20

	# 查询数据
	jobs_data = search_job_list(current_user, form_data)
	import pprint
	pprint.pprint(jobs_data)
	return render_template('tjobs_list.html', jobs_data=jobs_data)
	
# 投递信息
@jobs.route('/delivery',methods=['POST'])
def delivery():
	if not hasattr(current_user, 'user_id') or not current_user.user_id:
		print("未登陆,拼接302重定向链接")
		redirect_url = url_for('iuser.login') + "?next=" + request.referrer
		print(redirect_url)
		return dRet(302, redirect_url)
	delivery_param = dict(request.form)
	return delivery_by_job_id(current_user, delivery_param)