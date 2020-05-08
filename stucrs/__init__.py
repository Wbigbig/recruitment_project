#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 项目的说明

from flask import Flask,request,render_template

from .project_utils import get_db_path,get_project_dir,datestr_to_timestamp,to_json

from .bp_main import main
from .bp_jobs import jobs
from .bp_companys import companys
from .bp_user import iuser

# 项目的配置信息
project_config = {}

# 读取文件中的配置信息
def read_file_config():
	pass
	
# 项目初始化工作
def project_starter():
	print('招聘网，starting...')
	
# 创建flask app 实例，以及配置蓝图模块
def create_app():
	project_config['basedir'] = get_project_dir()
	project_config['staticdir'] = get_project_dir()+'/static'
	project_config['templatesdir'] = get_project_dir()+'/templates'
	
	# 读取其他配置信息
	read_file_config()
	
	print(project_config)
	
	app = Flask(__name__,
		template_folder = project_config['templatesdir'],
		static_folder = project_config['staticdir'],
		static_url_path = ''
	)
	
	# 配置蓝图
	app.register_blueprint(blueprint=main)
	app.register_blueprint(blueprint=jobs,url_prefix='/jobs')
	app.register_blueprint(blueprint=companys,url_prefix='/companys')
	app.register_blueprint(blueprint=iuser, url_prefix='/iuser')
	
	
	# 执行项目初始化方法
	project_starter()
	
	return app
	
