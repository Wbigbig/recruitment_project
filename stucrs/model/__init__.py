#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/5/9 16:14
# Author  : W
# FileName: __init__.py.py
"""
增删改查，执行数据操作
"""

from flask_login import UserMixin
from .model_table import *
from stucrs.project_utils import dRet

import traceback

# 用户注册操作
def create_applicant_user(u_info):
    try:
        session.add(Applicant(**u_info))
        session.commit()
        session.close()
        print("applicant_add", u_info)
        return dRet(200, "注册成功", redirect_url='/iuser/main/')
    except:
        print(traceback.format_exc())
        return dRet(500, "用户注册操作异常")

class User(UserMixin):
    def __init__(self, login_param):
        print("实例化User", locals())
        self.user_id = None
        self.user_name = None
        self.phone = login_param.get("acc")
        self.password = login_param.get("password")
        self.email = login_param.get("acc")
        self.industry = None
        self.real_name = None
        self.birthday = None
        self.age = None
        self.city = None
        self.current_identity = None
        self.personal_experience = None
        self.educational_experience = None
        self.head_pic = None
        self.create_time = None

    # 验证账号密码
    def verify_password(self):
        print("验证账号")
        pe_user = self.get_phone_email_user()
        if not pe_user: return
        if self.password == pe_user.password:
            for k, v in vars(self).items():
                setattr(self, k, getattr(pe_user, k))   # 密码正确，重置用户信息
            setattr(self, "id", self.user_id)           # 设置实例id，用户login_user需要使用
            return True
        return

    def get_phone_email_user(self):
        """
        尝试从数据库获取用户信息
        :return: 返回None则无对应用户
        """
        try:
            print("获取用户信息")
            user_ret = session.query(Applicant).filter(or_(Applicant.phone == self.phone, Applicant.email == self.email)).first()
            if not user_ret: return
            return user_ret
        except:
            pass

    # 注册用户
    @staticmethod
    def create_user(register_param):
        try:
            print("注册账号", locals())
            if session.query(Applicant).filter(Applicant.phone == register_param["phone"]).first():
                return dRet(500, "该手机号已注册")
            if session.query(Applicant).filter(Applicant.email == register_param["email"]).first():
                return dRet(500, "该邮箱号已注册")
            return create_applicant_user(register_param)
        except:
            return dRet(500, "注册异常！")

    @staticmethod
    def get(user_id):
        """
        尝试返回用户id对应的用户对象。加载用户回调函数使用此方法
        :param user_id:
        :return:
        """
        try:
            print("用户回调User.get", user_id)
            user_ret = session.query(Applicant).filter(Applicant.user_id == user_id).first()
            user_get = User({"acc": user_ret.phone, "password": user_ret.password})
            user_get.verify_password()
            return user_get
        except:
            return

# 用户个人信息更新操作
def update_applicant_user(current_user, iu_param):
    try:
        print("更新用户信息", current_user.user_id, iu_param)
        session.query(Applicant).filter(Applicant.user_id == current_user.user_id).update(iu_param)
        session.commit()
        session.close()
        return dRet(200, "更新成功", redirect_url='/iuser/main/')
    except:
        print(traceback.format_exc())
        return dRet(500, "更新异常")

# 获取用户投递记录
def get_delivery_record(current_user):
    try:
        print("获取用户投递记录", current_user.user_id)
        records = session.query(DeliveryRecord).filter(DeliveryRecord.user_id == current_user.user_id).order_by(DeliveryRecord.delivery_time.desc()).all()
        delivery_record_list = []
        for record in records:
            t_rec = {
                "company_name": record.recruiter_company.company_name,
                "job_title": record.recruitment_position.job_title,
                "education_requirements": record.recruitment_position.education_requirements,
                "salary_range": record.recruitment_position.salary_range,
                "job_description": record.recruitment_position.job_description,
                "work_address": record.recruitment_position.work_address,
                "delivery_time": record.delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
                "hr_real_name": record.recruiter_hr.real_name,
                "state": "-",
                "data": 1
            }
            delivery_record_list.append(t_rec)
        # 不足10条补齐10条
        if len(records) < 10:
            for _ in range(10-len(records)):
                delivery_record_list.append({
                "company_name": "-",
                "job_title": "-",
                "education_requirements": "-",
                "salary_range": "-",
                "job_description": "-",
                "work_address": "-",
                "delivery_time": "-",
                "hr_real_name": "-",
                "state": "-",
                "data": 0
            })
        session.close()
        print("投递记录", current_user.user_id, delivery_record_list)
        return dRet(200, delivery_record_list)
    except:
        print(traceback.format_exc())
        return dRet(500, "获取投递记录异常")

# 获取应聘者工作经历
def get_work_experience(current_user):
    try:
        print("获取用户工作经历", current_user.user_id)
        experiences = session.query(WorkExperience).filter(WorkExperience.user_id == current_user.user_id).order_by(WorkExperience.create_time.desc()).all()
        experiences_list = []
        for experience in experiences:
            t_exp = {}
            for k,v in vars(experience).items():
                t_exp[k] = v
            experiences_list.append(t_exp)
        session.close()
        print("工作经历", current_user.user_id, experiences_list)
        return dRet(200, experiences_list, total=len(experiences_list))
    except:
        print(traceback.format_exc())
        return dRet(500, "获取工作经历异常")

# 获取应聘者收藏表
def get_position_heart(current_user):
    try:
        print("获取用户收藏记录", current_user.user_id)
        position_hearts = session.query(heartPosition).filter(heartPosition.user_id == current_user.user_id).all()
        hearts_list = []
        for heart in position_hearts:
            ret_position = filter_from_model_by_kw(RecruitmentPosition, job_id=heart.job_id)
            if not ret_position: continue
            hearts_list.append({
                "job_id": ret_position.job_id,
                "job_title": ret_position.job_title,
                "company_name": ret_position.recruiter_company.company_name,
                "work_city": ret_position.work_city,
                "salary_range": ret_position.salary_range,
                "hr_name": ret_position.recruiter_hr.name,
                "create_time": ret_position.create_time.strftime("%Y-%m-%d %H:%M")
            })
        return dRet(200, hearts_list)
    except:
        print(traceback.format_exc())
        return dRet(500, "获取收藏记录异常")

# 判断we_id是否在归属该用户
def eq_we_id_in_work_experience(current_user, form_data):
    try:
        print("判断we_id归属", current_user.user_id, form_data)
        for experience in get_work_experience(current_user).get('data'):
            if experience['we_id'] == int(form_data['we_id']):
                return dRet(200, experience)
        return dRet(500, "该用户不存在此数据")
    except:
        print(traceback.format_exc())
        return dRet(500, "判断we_id归属异常")

# 修改或保存应聘者工作经历
def save_work_experience(current_user, form_data):
    try:
        if form_data['we_id'] != '0':
            # 执行修改操作
            print("执行更新工作经历操作", current_user.user_id, form_data)
            eq_ret = eq_we_id_in_work_experience(current_user, form_data)
            if eq_ret['status'] == 200:
                update_experience_info = {
                    "company_name": None,
                    "company_industry": None,
                    "entry_time": None,
                    "departure_time": None,
                    "job_title": None,
                    "department": None,
                    "job_content": None,
                }
                for k in update_experience_info.keys():
                    update_experience_info[k] = form_data[k]
                session.query(WorkExperience).filter(WorkExperience.we_id == int(form_data['we_id'])).update(update_experience_info)
                session.commit()
                session.close()
                return dRet(200, "修改成功")
            return eq_ret
        print("执行新增工作经历操作", current_user.user_id, form_data)
        form_data['we_id'] = int(form_data['we_id'])
        form_data['user_id'] = current_user.user_id
        print(form_data)
        session.add(WorkExperience(**form_data))
        session.commit()
        session.close()
        return dRet(200, "新增成功")
    except:
        print(traceback.format_exc())
        return dRet(500, "新增或保存工作经历异常")

# 删除用户工作经历
def remove_work_experience(current_user, form_data):
    try:
        print("执行删除工作经历操作", current_user.user_id, form_data)
        eq_ret = eq_we_id_in_work_experience(current_user, form_data)
        if eq_ret['status'] == 200:
            session.query(WorkExperience).filter(WorkExperience.we_id == int(form_data['we_id'])).delete()
            session.commit()
            session.close()
            return dRet(200, "删除成功")
        return eq_ret
    except:
        print(traceback.format_exc())
        return dRet(500, "删除工作经历异常")

# 删除用户收藏
def remove_position_heart(current_user, form_data):
    try:
        print("执行删除收藏操作", current_user.user_id, form_data)
        ret_heart = filter_from_model_by_kw(heartPosition, user_id=current_user.user_id, job_id=int(form_data["job_id"]))
        if not ret_heart:
            return dRet(500, "无该数据")
        session.query(heartPosition).filter(and_(heartPosition.user_id==current_user.user_id,heartPosition.job_id==int(form_data["job_id"]))).delete()
        session.commit()
        session.close()
        return  dRet(200, "已取消收藏该职位")
    except:
        print(traceback.format_exc())
        return dRet(500, "删除收藏异常")

# 查询职位列表job_list
def search_job_list(current_user, form_data):
    try:
        print("查询职位列表操作", form_data)
        search_ = []
        # 多表查询 RecruitmentPosition, RecruiterCompany, RecruiterHr
        search_.append(and_(RecruitmentPosition.company_id == RecruiterCompany.company_id, RecruitmentPosition.hr_id == RecruiterHr.hr_id))
        if form_data['start_time']:
            start_time = datetime.datetime.strptime(form_data['start_time']+" 00:00:00", "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(form_data['end_time']+" 23:59:59", "%Y-%m-%d %H:%M:%S")
            search_.append(and_(RecruitmentPosition.create_time>=start_time, RecruitmentPosition.create_time<=end_time))
        if form_data['education_requirements']:
            search_.append(RecruitmentPosition.education_requirements.like('%{0}%'.format(form_data['education_requirements'])))
        if form_data['company_industry']:
            search_.append(RecruiterCompany.company_industry.like('%{0}%'.format(form_data['company_industry'])))
        if form_data['work_city']:
            search_.append(RecruitmentPosition.work_city.like('%{0}%'.format(form_data['work_city'])))
        # 获取总数
        jobs_total = session.query(RecruitmentPosition, RecruiterCompany, RecruiterHr)\
            .filter(*search_)\
            .count()
        # 计算总页数
        page_total = jobs_total // form_data['pagesize']
        if jobs_total % form_data['pagesize'] != 0:
            page_total+=1
        # 根据分页查询数据
        job_list = session.query(RecruitmentPosition, RecruiterCompany, RecruiterHr)\
            .filter(*search_)\
            .order_by(RecruitmentPosition.create_time.desc())\
            .limit(form_data['pagesize']).offset((form_data['page']-1)*form_data['pagesize'])
        job_list_ret = []
        for job in job_list:
            tem_job = {}
            tem_job['job_id'] = job.RecruitmentPosition.job_id
            tem_job['job_title'] = job.RecruitmentPosition.job_title
            tem_job['company_name'] = job.RecruiterCompany.company_name
            tem_job['work_city'] = job.RecruitmentPosition.work_city
            tem_job['salary_range'] = job.RecruitmentPosition.salary_range
            tem_job['hr_name'] = job.RecruiterHr.name
            tem_job['create_time'] = job.RecruitmentPosition.create_time.strftime("%Y-%m-%d %H:%M")
            job_list_ret.append(tem_job)
        # 翻页列表
        pagenumbers = []
        for i in range(form_data['page'] - 3, form_data['page'] + 4):
            if i < 1:
                continue
            if i > page_total:
                continue
            pagenumbers.append(i)
        print(job_list_ret, len(job_list_ret))
        jobs_info_ret = {
            'jobs_total': jobs_total,
            'page_total': page_total,
            'pagenumbers': pagenumbers,
            'jobs_list': job_list_ret,
            'pagesize_list': [20, 30, 50, 100]  # 单页数量
        }
        session.close()
        return dRet(200, jobs_info_ret, search_param=form_data)
    except:
        print(traceback.format_exc())
        return dRet(500, "查询职位列表异常")

# 查询公司列表company_list
def search_company_list(current_user, form_data):
    try:
        print("查询公司列表操作", form_data)
        search_ = []
        if form_data['company_name']:
            search_.append(RecruiterCompany.company_name.like('%{0}%'.format(form_data['company_name'])))
        if form_data['company_industry']:
            search_.append(RecruiterCompany.company_industry.like('%{0}%'.format(form_data['company_industry'])))
        if form_data['address']:
            search_.append(RecruiterCompany.address.like('%{0}%'.format(form_data['address'])))
        # 获取总数
        companys_total = session.query(RecruiterCompany).filter(*search_).count()
        # 计算总页数
        page_total = companys_total // form_data['pagesize'] if companys_total % form_data['pagesize'] == 0 else (companys_total // form_data['pagesize'] + 1)
        # 根据分页查询数据
        companys_list = session.query(RecruiterCompany).filter(*search_)\
            .order_by(RecruiterCompany.create_time.desc())\
            .limit(form_data['pagesize'])\
            .offset((form_data['page']-1)*form_data['pagesize'])
        companys_list_ret = []
        for company in companys_list:
            tem_company = {}
            for k,v in vars(company).items():
                if k == 'create_time':
                    tem_company[k]=v.strftime("%Y-%m-%d %H:%M")
                    continue
                tem_company[k] = v
            tem_company['position_count'] = len(company.rec_pos)
            companys_list_ret.append(tem_company)
        # 翻页列表
        pagenumbers = []
        for i in range(form_data['page'] - 3, form_data['page'] + 4):
            if i < 1:
                continue
            if i > page_total:
                continue
            pagenumbers.append(i)
        print(companys_list_ret, len(companys_list_ret))
        companys_info_ret = {
            'companys_total': companys_total,
            'page_total': page_total,
            'pagenumbers': pagenumbers,
            'companys_list': companys_list_ret,
            'pagesize_list': [20, 30, 50, 100]  # 单页数量
        }
        session.close()
        return dRet(200, companys_info_ret, search_param=form_data)
    except:
        print(traceback.format_exc())
        return dRet(500, "查询公司列表异常")

# 进行投递操作
def delivery_by_job_id(current_user, form_data):
    try:
        print("执行投递操作", current_user.user_id, form_data)
        # 根据job_id 获取详细信息
        job_data = session.query(RecruitmentPosition).filter(RecruitmentPosition.job_id == int(form_data['job_id'])).first()
        if not job_data:
            return dRet(500, "无该职位信息或该职位已撤销")
        # 判断是否重复投递
        if session.query(DeliveryRecord).filter(and_(DeliveryRecord.user_id == current_user.user_id, DeliveryRecord.job_id == int(form_data['job_id']))).first():
            print("重复投递")
            return dRet(500, "重复投递")
        deliver_info = {
            "user_id": current_user.user_id,
            "company_id": job_data.company_id,
            "job_id": int(form_data['job_id']),
            "hr_id": job_data.hr_id
        }
        session.add(DeliveryRecord(**deliver_info))
        session.commit()
        session.close()
        return dRet(200, "投递成功，可前往个人中心查看记录")
    except:
        print(traceback.format_exc())
        return dRet(500, "投递异常")

# 进行收藏操作
def heart_by_job_id(current_user, form_data):
    try:
        print("执行收藏职位操作", current_user.user_id, form_data)
        # 判断是否有该职位
        job_ret = filter_from_model_by_kw(RecruitmentPosition, job_id=int(form_data["job_id"]))
        if not job_ret:
            return dRet(500, "无该职位信息或该职位已撤销")
        # 判断是否重复收藏
        pos_heart_ret = filter_from_model_by_kw(heartPosition, user_id=current_user.user_id, job_id=int(form_data["job_id"]))
        if pos_heart_ret:
            return dRet(500, "重复收藏")
        heart_info = {
            "user_id": current_user.user_id,
            "job_id": int(form_data['job_id']),
        }
        session.add(heartPosition(**heart_info))
        session.commit()
        session.close()
        return dRet(200, "收藏成功")
    except:
        print(traceback.format_exc())
        return dRet(500, "收藏异常")


# 根据company_id 查找hr_id
def search_hr_id_by_company_id(company_id):
    hr = session.query(RecruiterHr).filter(RecruiterHr.company_id == company_id).first()
    session.close()
    return hr

# 根据job_id 查找职位信息
def search_job_details_by_job_id(job_id):
    position = filter_from_model_by_kw(RecruitmentPosition, job_id=int(job_id))
    if not position:
        return dRet(500, "该职位不存在")
    # 发布hr
    hr = filter_from_model_by_kw(RecruiterHr, hr_id=position.hr_id)
    # 归属公司
    company = hr.recruiter_company
    position_dict, hr_dict, company_dict = {}, {}, {}
    for k,v in vars(position).items():
        position_dict[k] = v
    for k,v in vars(hr).items():
        hr_dict[k] = v
    for k,v in vars(company).items():
        company_dict[k] = v
    ret = {
        "position": position_dict,
        "hr": hr_dict,
        "company": company_dict
    }
    return dRet(200, ret)

# 判断表是否存在该数据
def filter_from_model_by_kw(model, **kwargs):
    """

    :param model:
    :param kwargs:
    :return:
    """
    ret = session.query(model).filter_by(**kwargs).first()
    # session.close()
    return ret
