#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/5/9 12:10
# Author  : W
# FileName: model_table.py
# 模型层

"""
数据库连接、表模型创建
"""
import datetime

import traceback
from sqlalchemy import create_engine, or_,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

# 创建引擎
conn_str = "mysql+pymysql://{user}:{pwd}@localhost:3306/{db_name}?charset=utf8mb4"
connect_info = conn_str.format(user="root",
                               pwd="rootpwd",
                               db_name="recruitment_s")

ENGINE = create_engine(connect_info,
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=5,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       )
# 创建会话
Session = sessionmaker(bind=ENGINE)
session = Session()
# 创建基类
Base = declarative_base()

# 爬取公司信息表
# class spyderCompany(Base):
#     __tablename__ = "spyder_company"
#     company_id = Column(Integer, primary_key=True)
#     company_tag = Column(String(50))    # 国企/
#     company_name = Column(String(100), unique=True, index=True) # 简称
#     company_hold_name = Column(String(100), unique=True, index=True)    # 营业执照
#     company_industry = Column(String(50))   # 行业
#     phone = Column(String(11), unique=True)
#     address = Column(Text)  # 公司地址
#     establish_time = Column(String(50))
#     registered_capital = Column(String(50))
#     legal_representative = Column(String(50))
#     company_profile = Column(Text)      # 公司介绍
#     company_pic = Column(Text)
#     create_time = Column(DateTime, default=datetime.datetime.now)

# 首页搜索表
class spyderSearchMain(Base):
    __tablename__ = "spyder_mainsearch"
    job_id = Column(Integer, primary_key=True)
    job_name = Column(String(50), index=True)
    company_name = Column(String(100), index=True)
    company_link = Column(String(300))
    work_place = Column(String(50))
    salary = Column(String(50))
    puttime = Column(String(50))
    job_link = Column(String(300))
    create_time = Column(DateTime, default=datetime.datetime.now)

import time
# 搜索表入库操作
def insertSearchMain(job_list):
    try:
        add_list = []
        for job in job_list:
            # 过滤重复
            eq_st = time.time()
            if session.query(spyderSearchMain).filter(and_(spyderSearchMain.job_name == job["job_name"], spyderSearchMain.company_name == job["company_name"])).first():
                continue
            eq_et = time.time()
            print("对比时间%s秒" % (eq_et - eq_st))
            add_list.append(spyderSearchMain(**job))
        session.add_all(add_list)
        session.commit()
        session.close()
        print("applicant_add", len(add_list))
    except:
        print(traceback.format_exc())

# 企业招聘者HR
# class RecruiterHr(Base):
#     __tablename__ = "recruiter_hr"
#     hr_id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
#     name = Column(String(11), index=True)
#     real_name = Column(String(50))
#     phone = Column(String(50), unique=True)
#     password = Column(String(50))
#     email = Column(String(50), unique=True)
#     head_pic = Column(Text)
#     create_time = Column(DateTime, default=datetime.datetime.now)
#
#     # 与生成表结构无关，仅用于查询方便
#     recruiter_company = relationship("RecruiterCompany", backref="rec_hrs")

# 招聘职位信息
# class RecruitmentPosition(Base):
#     __tablename__ = "recruitment_position"
#     job_id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
#     hr_id = Column(Integer, ForeignKey("recruiter_hr.hr_id"), index=True)
#     job_title = Column(String(50), index=True)
#     work_province = Column(String(50))
#     work_city = Column(String(50))
#     work_address = Column(Text)
#     education_requirements = Column(String(50))
#     salary_range = Column(String(50))
#     job_description = Column(Text)
#     create_time = Column(DateTime, default=datetime.datetime.now)

def create_db():
    # 创建所有表
    Base.metadata.create_all(ENGINE)
    print("create finish")

def drop_db():
    # 删除所有表
    Base.metadata.drop_all(ENGINE)
    print("drop finish")

def drop_db_one(model):
    # 删除指定表
    model.__table__.drop(ENGINE)
    print("删除完成")


# drop_db_one(Applicant)
# drop_db()
# create_db()

import random

# 创建公司信息
def create_RecruiterCompany():
    company_info = {
        "company_name": "无敌生化2",
        "company_industry": "高科技",
        "phone": "".join([str(random.randint(0,9)) for _ in range(11)]),
        "address": "深圳市南山区高新技术园2",
        "establish_time": "2020-05-13",
        "registered_capital": "5亿",
        "legal_representative": "二八",
        "company_profile": "11111111111来了就是一家人，团结一致好家伙！冲冲冲！"
    }
    session.add(RecruiterCompany(**company_info))
    session.commit()
    session.close()
    print("创建公司完成")
# create_RecruiterCompany()

# 创建招聘者
def create_RecruiterHr():
    hr_info = {
        "company_id": 1,
        "name": "无敌生化2HR",
        "real_name": "任我闯",
        "phone": "".join([str(random.randint(0,9)) for _ in range(11)]),
        "password": "000000",
        "email": "hreamil2@163.com",
    }
    session.add(RecruiterHr(**hr_info))
    session.commit()
    session.close()
    print("创建HR完成")
# create_RecruiterHr()

# 创建招聘职位
def create_RecruitmentPosition():
    position_info = {
        "company_id": 2,
        "hr_id": 2,
        "job_title": "无敌生化工程师222",
        "work_province": "广东",
        "work_city": "佛山",
        "work_address": "深圳市南山区高新技术园粤海大道1号假的",
        "education_requirements": "本科",
        "salary_range": "100W/月薪",
        "job_description": "2222222222222熟读唐诗三百首！左青龙，右白虎！生化技术无所不能！干干干！"
    }
    session.add(RecruitmentPosition(**position_info))
    session.commit()
    session.close()
    print("创建职位完成")
# create_RecruitmentPosition()

# 创建投递记录
def create_DeliveryRecord():
    delivery_info = {
        "user_id": 3,
        "company_id": 1,
        "job_id": 1,
        "hr_id": 1
    }
    session.add(DeliveryRecord(**delivery_info))
    session.commit()
    session.close()
    print("创建投递记录完成")
# create_DeliveryRecord()

# 创建工作经历
def create_WorkExperience():
    work_experience_info = {
        "user_id": 3,
        "company_name": "电子化工领袖公司",
        "company_industry": "电子行业",
        "entry_time": "2018-06",
        "departure_time": "2020-06",
        "job_title": "电子工程师",
        "department": "电子技术部门",
        "job_content": "收到了开飞机稍等快乐就考虑大家快来就反抗来点实际分离开我我问解放路快递费但是是稍等快乐局我我的时间开心农场考虑就适乐肤\n对化工电子设备进行研究加工，实现公司以及客户的功能。为公司<br>创造伟大财富！实现自己的人生理想！冲冲冲！！！\nheieheieiehiehie收到了开飞机稍等快乐就考虑大家快来就反抗来点实际分离开我我问解放路快递费但是是稍等快乐局我我的时间开心农场考虑就适乐肤\n对化工电子设备进行研究加工，实现公司以及客户的功能。为公司创造伟大财富！实现自己的人生理想！冲冲冲！！！\nheieheieiehiehie收到了开飞机稍等快乐就考虑大家快来就反抗来点实际分离开我我问解放路快递费但是是稍等快乐局我我的时间开心农场考虑就适乐肤\n对化工电子设备进行研究加工，实现公司以及客户的功能。为公司创造伟大财富！实现自己的人生理想！冲冲冲！！！\nheieheieiehiehie收到了开飞机稍等快乐就考虑大家快来就反抗来点实际分离开我我问解放路快递费但是是稍等快乐局我我的时间开心农场考虑就适乐肤\n对化工电子设备进行研究加工，实现公司以及客户的功能。为公司创造伟大财富！实现自己的人生理想！冲冲冲！！！\nheieheieiehiehie",
    }
    session.add(WorkExperience(**work_experience_info))
    session.commit()
    session.close()
    print("创建工作经历完成")
# create_WorkExperience()


# 查询职位列表job_list
def search_job_list(current_user, form_data):
    try:
        # print("查询职位列表操作", current_user.user_id, form_data)
        print("1")
        search_ = []
        # 多表查询 RecruitmentPosition, RecruiterCompany, RecruiterHr
        search_.append(and_(RecruitmentPosition.company_id == RecruiterCompany.company_id, RecruitmentPosition.hr_id == RecruiterHr.hr_id))
        if form_data['start_time']:
            # dd = '2019-03-17 11:00:00'
            start_time = datetime.datetime.strptime(form_data['start_time'], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(form_data['end_time'], "%Y-%m-%d %H:%M:%S")
            search_.append(and_(RecruitmentPosition.create_time>=start_time, RecruitmentPosition.create_time<=end_time))
        if form_data['education_requirements']:
            search_.append(RecruitmentPosition.education_requirements.like('%{0}%'.format(form_data['education_requirements'])))
        if form_data['company_industry']:
            search_.append(RecruiterCompany.company_industry.like('%{0}%'.format(form_data['company_industry'])))
        if form_data['work_city']:
            search_.append(RecruitmentPosition.work_city.like('%{0}%'.format(form_data['work_city'])))
        job_list = session.query(RecruitmentPosition, RecruiterCompany, RecruiterHr).filter(*search_).all()
        job_list_ret = []
        for job in job_list:
            tem_job = {}
            tem_job['job_title'] = job.RecruitmentPosition.job_title
            tem_job['company_name'] = job.RecruiterCompany.company_name
            tem_job['work_city'] = job.RecruitmentPosition.work_city
            tem_job['salary_range'] = job.RecruitmentPosition.salary_range
            tem_job['create_time'] = job.RecruitmentPosition.create_time.strftime("%Y-%m-%d %H:%M")
            job_list_ret.append(tem_job)
        print(job_list_ret, len(job_list_ret))
        session.close()
    except:
        print(traceback.format_exc())
        # return dRet(500, "查询职位列表异常")
        pass

form_data = {
    'start_time': '2020-05-17 00:00:00',				# 发布时间 YYYY-MM-DD
    'end_time': '2020-05-17 18:31:00',					# 发布时间 YYYY-MM-DD
    'education_requirements': '',	# 学历要求
    'company_industry': '',			# 所属行业
    'work_city': '',				# 城市
}
# search_job_list(None, form_data)

print(0//2)
