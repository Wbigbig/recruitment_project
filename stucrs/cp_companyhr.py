#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

"""
构建 公司hr 主页 接口
"""

from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_required,current_user

from .project_utils import dRet
from .model import *

companyhr = Blueprint('companyhr',__name__)

@companyhr.route('/main/', methods=['GET'])
@login_required
def main():
    # 公司Hr主页, 个人信息
    hr = current_user
    # 获取职位被投递记录
    hr_deliveried_record = get_hr_deliveried_record(current_user).get('data')
    return render_template("companyhr_main.html", hr=hr, hr_deliveried_record=hr_deliveried_record)