#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图，新闻模块，/news

from flask import Blueprint,request,render_template
from .project_utils import get_db_path,datestr_to_timestamp,to_json
import sqlite3

jobs = Blueprint('jobs',__name__)

# 显示数据库表 ztest 中的记录
@jobs.route('/list',methods=['GET','POST'])
def list():
	if request.method=='POST':
		fclass = request.form.get('fclass') if ('fclass' in request.form) else ''
		kw = request.form.get('kw') if ('kw' in request.form) else ''
		date1 = request.form.get('date1') if ('date1' in request.form) else ''
		date2 = request.form.get('date2') if ('date2' in request.form) else ''
		
		
		
		# 翻页的两项
		page = request.form.get('page') if ('page' in request.form) else ''
		pagesize = request.form.get('pagesize') if ('pagesize' in request.form) else ''
	else:
		fclass = ''
		kw = ''
		date1 = ''
		date2 = ''
		
		page=''
		pagesize=''
		
		
	# 日期的字符串转为时间戳，进行数据库的查询
	try:
		ftime1 = datestr_to_timestamp(date1,format='%Y-%m-%d') if date1!='' else 0
		ftime2 = datestr_to_timestamp(date2,format='%Y-%m-%d') if date2!='' else 0
	except:
		ftime1 = 0
		ftime2 = 0
		
	# 分页的转换单独写
	try:
		page = int(page)
		pagesize = int(pagesize)
	except:
		page=1
		pagesize=10
		
	
		
	# 将页面上需要的数据统一放到数据模型 data modal 中,字典
	dm = {}
	dm['fclass']=fclass
	dm['kw']=kw
	dm['date1'] = date1
	dm['date2'] = date2
	dm['page']=page
	dm['pagesize']=pagesize


	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
	
	# 所有的栏目需要传递给页面，形成下拉列表使用
	sql = '''
		select distinct fclass from tnews
	'''
	result = cursor.execute(sql).fetchall()
	allclasses = [x[0] for x in result]
	dm['allclasses'] = allclasses
	
	
	# 定义一个查询条件的字典
	dt_conn = {}
	
	# 翻页需要先找到满足条件的记录有多少条
	sql = '''
	select count(*) from tnews where 1=1
	'''
	
	if fclass!='':
		sql += ' and fclass=:fclass'
		dt_conn['fclass']=fclass
	if kw!='':
		sql += ' and (title like :kw or content like :kw)'
		dt_conn['kw']='%'+kw+'%'
	if ftime1>0:
		sql += ' and ftime>=:ftime1'
		dt_conn['ftime1']=ftime1
	if ftime2>0:
		sql += ' and ftime<=:ftime2'
		dt_conn['ftime2']=ftime2
		
	result_one = cursor.execute(sql,dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	dm['total']=total
	
	# 本页数据内容的查询，当 total>0 时进行
	if total>0:
	
		sql = '''
		select id,title,fdate,fclass,clickrate from tnews where 1=1
		'''
		
		if fclass!='':
			sql += ' and fclass=:fclass'
			dt_conn['fclass']=fclass
		if kw!='':
			sql += ' and (title like :kw or content like :kw)'
			dt_conn['kw']='%'+kw+'%'
		if ftime1>0:
			sql += ' and ftime>=:ftime1'
			dt_conn['ftime1']=ftime1
		if ftime2>0:
			sql += ' and ftime<=:ftime2'
			dt_conn['ftime2']=ftime2
			
		# 根据时间 ftime 排序
		sql += ' order by ftime desc'
			
		# 加上翻页的sql
		sql += ' limit '+str(pagesize)+' offset '+str((page-1)*pagesize)
			
		print(sql)
		
		result = cursor.execute(sql,dt_conn).fetchall()
		print(result)
		
		# 将内部的元组转换为字典
		# 将表字段使用列表形式保存，便于后续的循环匹配
		rows = []
		for line in result:
			record = {}
			record['id']=line[0]
			record['title']=line[1]
			record['fdate']=line[2]
			record['fclass']=line[3]
			record['clickrate']=line[4]
			
			rows.append(record)
			
		dm['rows']=rows
		
		#计算总共有多少页
		totalpage = total // pagesize
		if total % pagesize != 0:
			totalpage+=1
		dm['totalpage']=totalpage
		
		#翻页显示前三后三，需要使用列表
		pagenumbers=[]
		for i in range(page-3,page+4):
			if i<1:
				continue
			if i>totalpage:
				continue
			pagenumbers.append(i)
			
		print(pagenumbers)
		
		dm['pagenumbers']=pagenumbers
		

	# 关闭数据库
	conn.close()
	
	print(dm)
		
	return render_template('tnews_list.html',dm=dm)
	
# 增加修改前，获得数据内容
@jobs.route('/presave',methods=['POST'])
def presave():
	# 数据库记录的id号，>0表示修改
	id = request.form.get('id') if ('id' in request.form) else ''
	try:
		id = int(id)
	except:
		id = 0
		
	# 返回给页面的，一条数据记录，指定默认值
	# 新增的情况，返回默认值
	record = {}
	record['id']=0
	record['title']=''
	record['content']=''
	record['fdate']=''
	record['ftime']=0
	record['fclass']=''
	record['clickrate']=0
	
	if id>0:
		# 修改的情况，需要从数据库获得记录的数据
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		select * from tnews where id=?
		'''
		result_one = cursor.execute(sql,(id,)).fetchone()
		if result_one is not None:
			record['id']=result_one[0]
			record['title']=result_one[1]
			record['content']=result_one[2]
			record['fdate']=result_one[3]
			record['ftime']=result_one[4]
			record['fclass']=result_one[5]
			record['clickrate']=result_one[6]
			
		conn.close()
		
	# 以json数据的形式返回
	return to_json(succ=True,record=record)
	
# 保存数据库
@jobs.route('/save',methods=['POST'])
def save():
	id = request.form.get('id') if ('id' in request.form) else ''
	fclass = request.form.get('fclass') if ('fclass' in request.form) else ''
	title = request.form.get('title') if ('title' in request.form) else ''
	fdate = request.form.get('fdate') if ('fdate' in request.form) else ''
	content = request.form.get('content') if ('content' in request.form) else ''
	
	try:
		id = int(id)
	except:
		id = 0
		
	# 需要通过日期得到时间戳，这里可能会又异常
	try:
		ftime = datestr_to_timestamp(fdate,format='%Y-%m-%d')
	except:
		# 发送异常，直接返回错误信息
		return to_json(succ=False,stmt='日期格式错误:{}'.format(fdate))
		
	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
		
	if id>0:
		# 修改
		sql = '''
		update tnews set fclass=?,title=?,fdate=?,ftime=?,content=? where id=?
		'''
		cursor.execute(sql,(fclass,title,fdate,ftime,content,id))
	else:
		# 新增
		sql = '''
		insert into tnews(title,content,fdate,ftime,fclass,clickrate) 
		values(?,?,?,?,?,?)
		'''
		cursor.execute(sql,(title,content,fdate,ftime,fclass,0))
		
	conn.commit()
	conn.close()
	
	# json形式返回成功
	return to_json(succ=True)
	
# 删除
@jobs.route('/remove',methods=['POST'])
def remove():
	id = request.form.get('id') if ('id' in request.form) else ''
	
	try:
		id = int(id)
	except:
		id = 0
		
	# 删除必须根据id号
	if id>0:
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		delete from tnews where id=?
		'''
		cursor.execute(sql,(id,))
		conn.commit()
		conn.close()
		
	# json形式返回成功
	return to_json(succ=True)
	
# 新闻的详情页面
@jobs.route('/detail')
def detail():
	id = request.args.get('id') if ('id' in request.args) else ''
	try:
		id = int(id)
	except:
		id = 0
		
	
		
	#根据id号查询新闻记录信息
	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
	
	# 每次打开该新闻，点击量就加1
	sql = '''
	update tnews set clickrate=clickrate+1 where id=?
	'''
	cursor.execute(sql,(id,))
	
	
	# 根据id号查询新闻记录信息
	sql = '''
	select * from tnews where id=?
	'''
	result_one = cursor.execute(sql,(id,)).fetchone()
	
	# 及时更新
	conn.commit()
	conn.close()
	
	if result_one is None:
		return '新闻信息不存在. id={}'.format(id)
		
	# 将元组转成字典
	record = {}
	record['id']=result_one[0]
	record['title']=result_one[1]
	record['content']=result_one[2]
	record['fdate']=result_one[3]
	record['ftime']=result_one[4]
	record['fclass']=result_one[5]
	record['clickrate']=result_one[6]
	
	return render_template('tnews_detail.html',dm=record)
	