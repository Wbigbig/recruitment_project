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

# 爬取公司信息表
class spyderCompany(Base):
    __tablename__ = "spyder_company"
    company_id = Column(Integer, primary_key=True)
    company_tag = Column(String(50))    # 国企/
    company_name = Column(String(100), unique=True, index=True) # 简称
    company_hold_name = Column(String(100), unique=True, index=True)    # 营业执照
    company_industry = Column(String(50))   # 行业
    phone = Column(String(11), unique=True)
    address = Column(Text)  # 公司地址
    establish_time = Column(String(50))
    registered_capital = Column(String(50))
    legal_representative = Column(String(50))
    company_profile = Column(Text)      # 公司介绍
    company_link = Column(String(300))  # 链接
    company_pic = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)
    howmany_people = Column(String(50))
    company_web = Column(String(300))

# 查询是否有该公司,有则返回id,无则返回0，异常None
def search_or_create_spydercompany(searchjob):
    try:
        ret_company = session.query(spyderCompany).filter(spyderCompany.company_name == searchjob.company_name).first()
        session.close()
        if not ret_company:
            return 0
        return ret_company.company_id
    except:
        return None

# addspyderCompany 新增公司 返回新增公司
def add_spyderCompany(company_info):
    try:
        session.add(spyderCompany(**company_info))
        session.commit()
        ret_company = session.query(spyderCompany).order_by(spyderCompany.company_id.desc()).first()
        session.close()
        return ret_company
    except:
        session.close()
        print(traceback.format_exc())
        return None

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
    company_id = Column(Integer)
    jobinfo_id = Column(Integer)


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

# 计算搜索表总数，分页总数
def get_total_ptotal_from_searchmain(pagesize):
    """
    :param pagesize:单页数量
    :return: total，totalpage
    """
    try:
        total = session.query(spyderSearchMain).count()
        pagetotal = total // pagesize if total % pagesize == 0 else total // pagesize + 1
        return total, pagetotal
    except:
        print(traceback.format_exc())
        return

# 获取搜索表指定页码数据
def get_search_main_by_page(page, pagesize, pagetotal):
    """
    根据pagesize分页返回指定page数据
    :param page:
    :param pagesize:
    :return:
    """
    try:
        if page < 1 or page > pagetotal:
            print("页码异常")
            return None
        ret = session.query(spyderSearchMain).order_by(spyderSearchMain.job_id).limit(pagesize).offset((page - 1) * pagesize)
        session.close()
        return ret
    except:
        print(traceback.format_exc())
        return

# 更新spyderSearchMain数据表company_id字段,jobinfo_id字段
def update_spyderSearchMain_company_jobinfo_id(job, key):
    session.query(spyderSearchMain).filter(spyderSearchMain.job_id == job.job_id).update({key:getattr(job,key)})# update是字典
    session.commit()
    session.close()


# 爬虫招聘职位信息
class spyderRecruitmentPosition(Base):
    __tablename__ = "spyder_recruitment_position"
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("spyder_company.company_id"), index=True)
    job_title = Column(String(50), index=True)
    work_province = Column(String(50))
    work_city = Column(String(50))          # 城市
    work_address = Column(Text)             # 上班地址
    work_experience_requirements = Column(String(50))   # 经验要求
    education_requirements = Column(String(50))     # 学历要求
    salary_range = Column(String(50))   # 薪资范围
    job_description = Column(Text)      # 职位信息
    job_persion_requirements = Column(String(50))   # 招聘人数
    job_puttime = Column(String(50))        # 发布时间
    job_link = Column(String(300))
    create_time = Column(DateTime, default=datetime.datetime.now)

    # 与spyder公司的正反向查询
    spyder_company = relationship("spyderCompany", backref="backpos")

# 查询公司是否有该职位id
def search_job_from_spydercompany(job):
    try:
        company_belong = session.query(spyderCompany).filter(spyderCompany.company_id == job.company_id).first()
        for jobinfo in company_belong.backpos:
            if job.job_name == jobinfo.job_title and job.job_link == jobinfo.job_link:
                return jobinfo.job_id
        return 0
    except:
        print(traceback.format_exc())
        return None

# 新增职位
def add_spyderRecruitmentPosition(job_info):
    try:
        session.add(spyderRecruitmentPosition(**job_info))
        session.commit()
        ret_job = session.query(spyderRecruitmentPosition).order_by(spyderRecruitmentPosition.job_id.desc()).first()
        session.close()
        return ret_job
    except:
        session.close()
        print(traceback.format_exc())
        return None

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

