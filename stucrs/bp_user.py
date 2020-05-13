#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 用户信息接口蓝图，构建在：/iuser

from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_user,logout_user,login_required,current_user

from .project_utils import get_db_path,datestr_to_timestamp,to_json,dRet,get_next
from .model import User, update_applicant_user, get_delivery_record

import re
import sqlite3

iuser = Blueprint('iuser',__name__)

@iuser.route('/login/', methods=['POST','GET'])
def login():
	# 获取登录信息
	login_param = request.get_json()
	print(login_param)
	if login_param:
		lg_user = User(login_param)
		if lg_user.verify_password():
			print("存储用户登录状态", lg_user.user_name, lg_user.phone, lg_user.email)
			login_user(lg_user, remember=True)
			print(dRet(200, "成功"))
			ref_next = get_next(request.referrer)
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

@iuser.route('/verifyLogin/', methods=['POST'])
@login_required
def verify_login():
	# 测试登录状态是否成功
	return dRet(200, "维持登录中")

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
		# iu_delivery_record = [
		# 	{
		# 		"company_name": i,
		# 		"job_title": i,
		# 		"education_requirements": i,
		# 		"salary_range": i,
		# 		"job_description": i,
		# 		"work_address": i,
		# 		"delivery_time": i,
		# 		"hr_real_name": i
		# 	} for i in range(10)
		# ]
		return render_template("iuser_main.html", iu=iu, iu_delivery_record=iu_delivery_record)

# 更新修改用户信息
@iuser.route('/iu_update',methods=['POST'])
@login_required
def iu_update():
	iu_param = request.get_json()
	return update_applicant_user(current_user, iu_param)

@iuser.route('/list/',methods=['GET','POST'])
@login_required
def list():
	if request.method=='POST':
		kw = request.form.get('kw', '')

		# 翻页的两项
		page = request.form.get('page') if ('page' in request.form) else ''
		pagesize = request.form.get('pagesize') if ('pagesize' in request.form) else ''
	else:
		kw = ''

		page=''
		pagesize=''


	# 分页的转换单独写
	try:
		page = int(page)
		pagesize = int(pagesize)
	except:
		page = 1
		pagesize = 10

	# 将页面上需要的数据统一放到数据模型 data modal 中,字典
	dm = {}
	dm['kw'] = kw
	dm['page'] = page
	dm['pagesize'] = pagesize

	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()

	# 定义一个查询条件的字典
	dt_conn = {}

	# 翻页需要先找到满足条件的记录有多少条
	sql = '''
		select count(*) from tcourse where 1=1
		'''


	if kw != '':
		sql += ' and (code like :kw or name like :kw)'
		dt_conn['kw'] = '%' + kw + '%'

	print(dt_conn)

	result_one = cursor.execute(sql, dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	dm['total'] = total

	# 本页数据内容的查询，当 total>0 时进行
	if total > 0:

		sql = '''
			select id,code,name,score,institute from tcourse where 1=1
			'''

		if kw != '':
			sql += ' and (code like :kw or name like :kw)'	# 编码 或 课程名称模糊搜索
			dt_conn['kw'] = '%' + kw + '%'

		# 加上翻页的sql
		sql += ' limit ' + str(pagesize) + ' offset ' + str((page - 1) * pagesize)

		print(sql)

		result = cursor.execute(sql, dt_conn).fetchall()
		print(result)

		# 将内部的元组转换为字典
		# 将表字段使用列表形式保存，便于后续的循环匹配
		rows = []
		for line in result:
			record = {}
			record['id'] = line[0]
			record['code'] = line[1]
			record['name'] = line[2]
			record['score'] = line[3]
			record['institute'] = line[4]

			rows.append(record)

		dm['rows'] = rows

		# 计算总共有多少页
		totalpage = total // pagesize
		if total % pagesize != 0:
			totalpage += 1
		dm['totalpage'] = totalpage

		# 翻页显示前三后三，需要使用列表
		pagenumbers = []
		for i in range(page - 3, page + 4):
			if i < 1:
				continue
			if i > totalpage:
				continue
			pagenumbers.append(i)

		print(pagenumbers)

		dm['pagenumbers'] = pagenumbers

	# 关闭数据库
	conn.close()

	print(dm)


	return render_template('iuser_main.html', dm=dm)


# 增加修改前，获得数据内容
@iuser.route('/presave', methods=['POST'])
def presave():
	# 数据库记录的id号，>0表示修改
	id = request.form.get('id', '')
	try:
		id = int(id)
	except:
		id = 0

	# 返回给页面的，一条数据记录，指定默认值
	# 新增的情况，返回默认值
	record = {}
	record['id'] = 0
	record['code'] = ''
	record['name'] = ''
	record['score'] = ''
	record['institute'] = ''

	if id > 0:
		# 修改的情况，需要从数据库获得记录的数据
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		select * from tcourse where id=?
		'''
		result_one = cursor.execute(sql, (id,)).fetchone()
		if result_one is not None:
			record['id'] = result_one[0]
			record['code'] = result_one[1]
			record['name'] = result_one[2]
			record['score'] = result_one[3]
			record['institute'] = result_one[4]

		conn.close()

	# 以json数据的形式返回
	return to_json(succ=True, record=record)


# 保存数据库
@iuser.route('/save', methods=['POST'])
def save():
	id = request.form.get('id', '')
	code = request.form.get('code', '')
	name = request.form.get('name', '')
	score = request.form.get('score', '')
	institute = request.form.get('institute', '')


	try:
		id = int(id)
	except:
		id = 0

	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()

	if id > 0:
		# 修改
		sql = '''
		update tcourse set code=?,name=?,score=?,institute=? where id=?
		'''
		cursor.execute(sql, (code, name, score, institute, id))
	else:
		# 新增
		sql = '''
		insert into tcourse(code, name, score, institute)
		values(?,?,?,?)
		'''
		cursor.execute(sql, (code, name, score, institute))

	conn.commit()
	conn.close()

	# json形式返回成功
	return to_json(succ=True)


# 删除
@iuser.route('/remove', methods=['POST'])
def remove():
	id = request.form.get('id', '')

	try:
		id = int(id)
	except:
		id = 0

	# 删除必须根据id号
	if id > 0:
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		delete from tcourse where id=?
		'''
		cursor.execute(sql, (id,))
		conn.commit()
		conn.close()

	# json形式返回成功
	return to_json(succ=True)


