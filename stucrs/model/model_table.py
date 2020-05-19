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
Session = sessionmaker(bind=ENGINE,expire_on_commit=False)
session = Session()
# 创建基类
Base = declarative_base()

# 应聘者表
class Applicant(Base):
    __tablename__ = "applicant"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), index=True)
    phone = Column(String(11), unique=True, index=True)
    password = Column(String(50))
    email = Column(String(50), unique=True)
    industry = Column(String(50))
    real_name = Column(String(50))
    birthday = Column(String(50))
    age = Column(Integer)
    city = Column(String(50))
    current_identity = Column(String(50))
    personal_experience = Column(Text)
    educational_experience = Column(Text)
    head_pic = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

# 应聘者工作经历表
class WorkExperience(Base):
    __tablename__ = "work_experience"
    we_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("applicant.user_id"), index=True)
    company_name = Column(String(100))
    company_industry = Column(String(50))
    entry_time = Column(String(50))
    departure_time = Column(String(50))
    job_title = Column(String(50))
    department = Column(String(50))
    job_content = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

    # 与生成表结构无关，仅用于查询方便
    applicant = relationship("Applicant", backref="wes")

# 企业招聘者所属公司信息
class RecruiterCompany(Base):
    __tablename__ = "recruiter_company"
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(100), unique=True, index=True)
    company_industry = Column(String(50))
    phone = Column(String(11), unique=True)
    address = Column(Text)
    establish_time = Column(String(50))
    registered_capital = Column(String(50))
    legal_representative = Column(String(50))
    company_profile = Column(Text)
    company_pic = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

def get_total_ptotal_from_RecruiterCompany(pagesize):
    try:
        total = session.query(RecruiterCompany).count()
        session.close()
        pagetotal = total // pagesize if total % pagesize == 0 else total // pagesize + 1
        return total, pagetotal
    except:
        print(traceback.format_exc())
        return

def get_company_by_page(page, pagesize, pagetotal):
    try:
        if page < 1 or page > pagetotal:
            print("页码异常")
            return None
        ret = session.query(RecruiterCompany).order_by(RecruiterCompany.company_id).limit(pagesize).offset((page - 1) * pagesize)
        session.close()
        return ret
    except:
        print(traceback.format_exc())
        return

# 企业招聘者HR
class RecruiterHr(Base):
    __tablename__ = "recruiter_hr"
    hr_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
    name = Column(String(11), index=True)
    real_name = Column(String(50))
    phone = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(50), unique=True)
    head_pic = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

    # 与生成表结构无关，仅用于查询方便
    recruiter_company = relationship("RecruiterCompany", backref="rec_hrs")

# 招聘职位信息
class RecruitmentPosition(Base):
    __tablename__ = "recruitment_position"
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
    hr_id = Column(Integer, ForeignKey("recruiter_hr.hr_id"), index=True)
    job_title = Column(String(50), index=True)
    work_province = Column(String(50))
    work_city = Column(String(50))
    work_address = Column(Text)
    education_requirements = Column(String(50))
    salary_range = Column(String(50))
    job_description = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

    # 与生成表结构无关，仅用于查询方便
    recruiter_company = relationship("RecruiterCompany", backref="rec_pos")

    # 与HR信息的正反向查询
    recruiter_hr = relationship("RecruiterHr", backref="rec_pos")

# 投递记录表
class DeliveryRecord(Base):
    __tablename__ = "delivery_record"
    delivery_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("applicant.user_id"), index=True)
    company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
    job_id = Column(Integer, ForeignKey("recruitment_position.job_id"), index=True)
    hr_id = Column(Integer, ForeignKey("recruiter_hr.hr_id"), index=True)
    delivery_time = Column(DateTime, default=datetime.datetime.now)

    # 与生成表结构无关，仅用于查询方便
    # 与应聘者的正反向查询
    applicant = relationship("Applicant", backref="drs")

    # 与企业公司的正反向查询
    recruiter_company = relationship("RecruiterCompany", backref="drs")

    # 与职位信息的正反向查询
    recruitment_position = relationship("RecruitmentPosition", backref="drs")

    # 与HR信息的正反向查询
    recruiter_hr = relationship("RecruiterHr", backref="drs")

# 收藏表
class heartPosition(Base):
    __tablename__ = "recruitment_position_heart"
    heart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("applicant.user_id"), index=True)
    job_id = Column(Integer, index=True)    # 不能使用外键，若删除了job，收藏记录还是要有的
    create_time = Column(DateTime, default=datetime.datetime.now)

    # 与应聘者的正反向查询
    applicant = relationship("Applicant", backref="pos_heart")

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


########################### 测试创建数据
import random

# 创建公司信息
def create_RecruiterCompany(company_info):
    # company_info = {
    #     "company_name": "无敌生化2",
    #     "company_industry": "高科技",
    #     "phone": "".join([str(random.randint(0,9)) for _ in range(11)]),
    #     "address": "深圳市南山区高新技术园2",
    #     "establish_time": "2020-05-13",
    #     "registered_capital": "5亿",
    #     "legal_representative": "二八",
    #     "company_profile": "11111111111来了就是一家人，团结一致好家伙！冲冲冲！"
    # }
    session.add(RecruiterCompany(**company_info))
    session.commit()
    session.close()
    print("创建公司完成")
# create_RecruiterCompany()

# 创建招聘者
def create_RecruiterHr(hr_info):
    # hr_info = {
    #     "company_id": 1,
    #     "name": "无敌生化2HR",
    #     "real_name": "任我闯",
    #     "phone": "".join([str(random.randint(0,9)) for _ in range(11)]),
    #     "password": "000000",
    #     "email": "hreamil2@163.com",
    # }
    add_list = []
    for h in hr_info:
        add_list.append(RecruiterHr(**h))
    # session.add(RecruiterHr(**hr_info))
    session.add_all(add_list)
    session.commit()
    session.close()
    print("创建HR完成")
# create_RecruiterHr()

# 创建招聘职位
def create_RecruitmentPosition(position_info):
    # position_info = {
    #     "company_id": 2,
    #     "hr_id": 2,
    #     "job_title": "无敌生化工程师222",
    #     "work_province": "广东",
    #     "work_city": "佛山",
    #     "work_address": "深圳市南山区高新技术园粤海大道1号假的",
    #     "education_requirements": "本科",
    #     "salary_range": "100W/月薪",
    #     "job_description": "2222222222222熟读唐诗三百首！左青龙，右白虎！生化技术无所不能！干干干！"
    # }
    add_list = []
    for p in position_info:
        add_list.append(RecruitmentPosition(**p))
    # session.add(RecruitmentPosition(**position_info))
    session.add_all(add_list)
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