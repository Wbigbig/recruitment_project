#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 公司信息蓝图，构建在：/stu

from flask import Blueprint,request,render_template,url_for
from flask_login import current_user

from stucrs.model import search_company_list
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

	# 查询数据
	companys_data = search_company_list(current_user, form_data)
	import pprint
	pprint.pprint(companys_data)
	return render_template('tcompany_list.html', companys_data=companys_data)


# 增加修改前，获得数据内容
@companys.route('/presave', methods=['POST'])
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
	record['birthday'] = ''
	record['age'] = ''
	record['institute'] = ''
	record['fclass'] = ''

	if id > 0:
		# 修改的情况，需要从数据库获得记录的数据
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		select * from tstudent where id=?
		'''
		result_one = cursor.execute(sql, (id,)).fetchone()
		if result_one is not None:
			record['id'] = result_one[0]
			record['code'] = result_one[1]
			record['name'] = result_one[2]
			record['birthday'] = result_one[3]
			record['age'] = result_one[4]
			record['institute'] = result_one[5]
			record['fclass'] = result_one[6]

		conn.close()

	# 以json数据的形式返回
	return to_json(succ=True, record=record)


# 保存数据库
@companys.route('/save', methods=['POST'])
def save():
	id = request.form.get('id', '')
	code = request.form.get('code', '')
	name = request.form.get('name', '')
	birthday = request.form.get('birthday', '')
	age = request.form.get('age', '')
	institute = request.form.get('institute', '')
	fclass = request.form.get('fclass', '')


	try:
		id = int(id)
	except:
		id = 0

	# 年龄字符串转为整形，进行数据库的查询
	try:
		age_i = int(age) if age != '' else 0
	except:
		age_i = 0

	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()

	if id > 0:
		# 修改
		sql = '''
		update tstudent set code=?,name=?,birthday=?,age=?,institute=?,fclass=? where id=?
		'''
		cursor.execute(sql, (code, name, birthday, age_i, institute, fclass, id))
	else:
		# 新增
		sql = '''
		insert into tstudent(code,name,birthday,age,institute,fclass)
		values(?,?,?,?,?,?)
		'''
		cursor.execute(sql, (code,name,birthday,age_i,institute,fclass))

	conn.commit()
	conn.close()

	# json形式返回成功
	return to_json(succ=True)


# 删除
@companys.route('/remove', methods=['POST'])
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
		delete from tstudent where id=?
		'''
		cursor.execute(sql, (id,))
		conn.commit()
		conn.close()

	# json形式返回成功
	return to_json(succ=True)

