#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/5/9 12:10
# Author  : W
# FileName: model_table.py
# 模型层

"""
数据库连接、表模型创建
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey

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

# 投递记录表
class DeliveryRecord(Base):
    __tablename__ = "delivery_record"
    delivery_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("applicant.user_id"), index=True)
    company_id = Column(Integer, ForeignKey("recruiter_company.company_id"), index=True)
    job_id = Column(Integer, ForeignKey("recruitment_position.job_id"), index=True)
    hr_id = Column(Integer, ForeignKey("recruiter_hr.hr_id"), index=True)
    delivery_time = Column(Integer)

    # 与生成表结构无关，仅用于查询方便
    # 与应聘者的正反向查询
    applicant = relationship("Applicant", backref="drs")

    # 与企业公司的正反向查询
    recruiter_company = relationship("RecruiterCompany", backref="drs")

    # 与职位信息的正反向查询
    recruitment_position = relationship("RecruitmentPosition", backref="drs")

    # 与HR信息的正反向查询
    recruiter_hr = relationship("RecruiterHr", backref="drs")

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

# create_db()
# drop_db_one(Applicant)
# drop_db()

