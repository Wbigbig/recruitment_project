#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/5/9 12:10
# Author  : W
# FileName: model_table.py
# 模型层

"""
数据库连接、表模型创建 爬虫表
"""

from stucrs.model.model_table import *

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
        session = Session()
        print(f'sessionid:{id(session)}')
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
        session = Session()
        print(f'sessionid:{id(session)}')
        session.add(spyderCompany(**company_info))
        session.commit()
        ret_company = session.query(spyderCompany).order_by(spyderCompany.company_id.desc()).first()
        session.close()
        return ret_company
    except:
        session.close()
        print(traceback.format_exc())
        return None

# 计算公司表总数，分页总数
def get_total_ptotal_from_spyderCompany(pagesize):
    try:
        session = Session()
        print(f'sessionid:{id(session)}')
        total = session.query(spyderCompany).count()
        pagetotal = total // pagesize if total % pagesize == 0 else total // pagesize + 1
        return total, pagetotal
    except:
        print(traceback.format_exc())
        return

# 获取公司表指定页码数据
def get_spyder_company_by_page(page, pagesize, pagetotal):
    """
    根据pagesize分页返回指定page数据
    :param page:
    :param pagesize:
    :return:
    """
    try:
        session = Session()
        print(f'sessionid:{id(session)}')
        if page < 1 or page > pagetotal:
            print("页码异常")
            return None
        ret = session.query(spyderCompany).order_by(spyderCompany.company_id).limit(pagesize).offset((page - 1) * pagesize)
        session.close()
        return ret
    except:
        print(traceback.format_exc())
        return


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
        session = Session()
        print(f'sessionid:{id(session)}')
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
        session = Session()
        print(f'sessionid:{id(session)}')
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
        session = Session()
        print(f'sessionid:{id(session)}')
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
    session = Session()
    print(f'sessionid:{id(session)}')
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
        session = Session()
        print(f'sessionid:{id(session)}')
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
        session = Session()
        print(f'sessionid:{id(session)}')
        session.add(spyderRecruitmentPosition(**job_info))
        session.commit()
        ret_job = session.query(spyderRecruitmentPosition).order_by(spyderRecruitmentPosition.job_id.desc()).first()
        session.close()
        return ret_job
    except:
        print(traceback.format_exc())
        return None

# 计算职位表总数，分页总数
def get_total_ptotal_from_postiton(pagesize):
    """
    :param pagesize:单页数量
    :return: total，totalpage
    """
    try:
        session = Session()
        print(f'sessionid:{id(session)}')
        total = session.query(spyderRecruitmentPosition).count()
        pagetotal = total // pagesize if total % pagesize == 0 else total // pagesize + 1
        return total, pagetotal
    except:
        print(traceback.format_exc())
        return

# 获取职位表指定页码数据
def get_position_by_page(page, pagesize, pagetotal):
    """
    根据pagesize分页返回指定page数据
    :param page:
    :param pagesize:
    :return:
    """
    try:
        session = Session()
        print(f'sessionid:{id(session)}')
        if page < 1 or page > pagetotal:
            print("页码异常")
            return None
        ret = session.query(spyderRecruitmentPosition).order_by(spyderRecruitmentPosition.job_id).limit(pagesize).offset((page - 1) * pagesize)
        session.close()
        return ret
    except:
        print(traceback.format_exc())
        return

# drop_db_one(RecruiterCompany)
# drop_db()
# create_db()