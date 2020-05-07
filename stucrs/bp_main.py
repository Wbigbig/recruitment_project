#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 主蓝图模块，构建在：/

from flask import Blueprint,request,render_template

main = Blueprint('main',__name__)

@main.route('/')
def index():
	return render_template('home.html')
	
@main.route('/login')
def login():
	return '用户登入'