#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 用户信息接口蓝图，构建在：/iuser

from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_user,logout_user,login_required,current_user

from .project_utils import dRet,get_next
from .model import User, update_applicant_user, get_delivery_record, get_work_experience, eq_we_id_in_work_experience, save_work_experience, remove_work_experience, get_position_heart, remove_position_heart

iuser = Blueprint('iuser',__name__)

@iuser.route('/login/', methods=['POST','GET'])
def login():
	# 获取登录信息
	login_param = request.get_json()
	print("登录参数", login_param)
	if login_param:
		lg_user = User(login_param)
		if lg_user.verify_password():
			print("存储用户登录状态", lg_user.user_name, lg_user.phone, lg_user.email)
			login_user(lg_user, remember=True)
			print(dRet(200, "成功"))
			ref_next = get_next(login_param, request.referrer)
			return dRet(200, "成功", redirect_url=ref_next)
		return dRet(500, "账号或密码错误")
	return render_template('login.html')

@iuser.route('/register/', methods=['POST','GET'])
def register():
	# 注册账号
	register_param = request.get_json()
	print(register_param)
	if register_param:
		rg_user = User.create_user(register_param)
		return rg_user
	return render_template('register.html')

@iuser.route('/logout/', methods=['POST','GET'])
def logout():
	# 注销账号
	logout_user()
	print(dRet(200, "登出成功"))
	return redirect(url_for('iuser.login'))

@iuser.route('/main/',methods=['GET','POST'])
@login_required
def main():
	# 个人中心
	if request.method == 'GET':
		# 获取用户信息
		iu = {
			"user_id": current_user.user_id,
			"user_name": current_user.user_name,
			"phone": current_user.phone,
			"password": current_user.password,
			"email": current_user.email,
			"industry": current_user.industry,
			"real_name": current_user.real_name,
			"birthday": current_user.birthday,
			"age": current_user.age,
			"city": current_user.city,
			"current_identity": current_user.current_identity,
			"personal_experience": current_user.personal_experience,
			"educational_experience": current_user.educational_experience,
			"head_pic": current_user.head_pic,
			"create_time": current_user.create_time
		}
		# 获取投递记录
		iu_delivery_record = get_delivery_record(current_user).get('data')
		# 获取工作经历
		iu_work_experience = get_work_experience(current_user)
		# 获取收藏记录
		iu_position_heart = get_position_heart(current_user).get('data')
		return render_template("iuser_main.html", iu=iu, iu_delivery_record=iu_delivery_record, iu_work_experience=iu_work_experience, iu_position_heart=iu_position_heart)

# 更新修改用户信息
@iuser.route('/iu_update',methods=['POST'])
@login_required
def iu_update():
	iu_param = request.get_json()
	return update_applicant_user(current_user, iu_param)

# 获取用户单个工作经历
@iuser.route('/work_experience_info',methods=['POST'])
@login_required
def work_experience_info():
	form_data = request.form
	eq_ret = eq_we_id_in_work_experience(current_user, form_data)
	if eq_ret['status'] == 500:
		return eq_ret
	ret_experience = {
		"we_id": None,
		"company_name": None,
		"company_industry": None,
		"entry_time": None,
		"departure_time": None,
		"job_title": None,
		"department": None,
		"job_content": None,
	}
	for k in ret_experience.keys():
		ret_experience[k] = eq_ret['data'][k]
	return dRet(200, ret_experience)

# 更新或保存用户工作经历
@iuser.route('/work_experience_save',methods=['POST'])
@login_required
def work_experience_save():
	form_data = dict(request.form)
	print("更新或保存用户工作经历:",form_data)
	return save_work_experience(current_user, form_data)

# 删除用户工作经历
@iuser.route('/work_experience_remove',methods=['POST'])
@login_required
def work_experience_remove():
	form_data = dict(request.form)
	return remove_work_experience(current_user, form_data)

# 删除用户收藏
@iuser.route('/position_heart_remove',methods=['POST'])
@login_required
def position_heart_remove():
	form_data = dict(request.form)
	return remove_position_heart(current_user, form_data)


