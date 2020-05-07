#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 学生信息蓝图，构建在：/stu

from flask import Blueprint,request,render_template
from .project_utils import get_db_path,datestr_to_timestamp,to_json
import sqlite3

stu = Blueprint('stu',__name__)

@stu.route('/list',methods=['GET','POST'])
def list():
	if request.method=='POST':
		kw = request.form.get('kw', '')
		age_min = request.form.get('age_min', '')
		age_max = request.form.get('age_max', '')

		# 翻页的两项
		page = request.form.get('page') if ('page' in request.form) else ''
		pagesize = request.form.get('pagesize') if ('pagesize' in request.form) else ''
	else:
		kw = ''
		age_min = ''
		age_max = ''

		page=''
		pagesize=''

	# 年龄字符串转为整形，进行数据库的查询
	try:
		age_min_i = int(age_min) if age_min != '' else 0
		age_max_i = int(age_max) if age_max != '' else 0
	except:
		age_min_i = 0
		age_max_i = 0

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
	dm['age_min'] = age_min
	dm['age_max'] = age_max
	dm['page'] = page
	dm['pagesize'] = pagesize

	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()

	# 定义一个查询条件的字典
	dt_conn = {}

	# 翻页需要先找到满足条件的记录有多少条
	sql = '''
		select count(*) from tstudent where 1=1
		'''


	if kw != '':
		sql += ' and (name like :kw)'
		dt_conn['kw'] = '%' + kw + '%'
	if age_min_i > 0:
		sql += ' and age>=:age_min_i'
		dt_conn['age_min_i'] = age_min_i
	if age_max_i > 0:
		sql += ' and age<=:age_max_i'
		dt_conn['age_max_i'] = age_max_i

	print(dt_conn)

	result_one = cursor.execute(sql, dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	dm['total'] = total

	# 本页数据内容的查询，当 total>0 时进行
	if total > 0:

		sql = '''
			select id,code,name,birthday,age,institute,fclass from tstudent where 1=1
			'''

		if kw != '':
			sql += ' and (name like :kw)'
			dt_conn['kw'] = '%' + kw + '%'
		if age_min_i > 0:
			sql += ' and age>=:age_min_i'
			dt_conn['age'] = age_min_i
		if age_max_i > 0:
			sql += ' and age<=:age_max_i'
			dt_conn['age'] = age_max_i

		# 根据时间 ftime 排序
		sql += ' order by age desc'

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
			record['birthday'] = line[3]
			record['age'] = line[4]
			record['institute'] = line[5]
			record['fclass'] = line[6]

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


	return render_template('stu_list.html', dm=dm)


# 增加修改前，获得数据内容
@stu.route('/presave', methods=['POST'])
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
@stu.route('/save', methods=['POST'])
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
@stu.route('/remove', methods=['POST'])
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

