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
    # 防止不同类型用户交叉访问页面
    if current_user.u_type == 0:return redirect(url_for("iuser.main"))
    # 公司Hr主页, 个人信息
    session = Session()
    current_user.company_name = session.query(RecruiterCompany.company_name).filter(RecruiterCompany.company_id == current_user.company_id).first()[0]
    hr = current_user
    # 获取职位被投递记录
    hr_deliveried_record = get_hr_deliveried_record(current_user).get('data')
    # 获取已发布职位信息
    hr_recruitment_position = get_hr_recruitment_position(current_user).get('data')
    return render_template("companyhr_main.html", hr=hr, hr_deliveried_record=hr_deliveried_record, hr_recruitment_position=hr_recruitment_position,main_route='/companyhr')

# 获取单个职位信息
@companyhr.route('/position_info', methods=['POST'])
@login_required
def position_info():
    form_data = request.form
    if form_data.get('job_id'):
        ret = search_job_details_by_job_id(int(form_data['job_id']))['data'].get('position')
        ret.pop('_sa_instance_state')
        ret.pop('recruiter_hr')
        return dRet(200, ret)
    return dRet(500, "参数错误")

# 更新或保存职位信息
@companyhr.route('/position_info_save',methods=['POST'])
@login_required
def position_info_save():
    form_data = dict(request.form)
    print("更新或保存职位信息", form_data)
    return save_position_info(current_user, form_data)

# 删除职位信息