#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 16:38
# Author  : W
# FileName: move_spyder_data.py
"""转移爬虫数据至生产表"""


from stucrs.model.spyder_model import get_total_ptotal_from_spyderCompany, get_spyder_company_by_page, \
    get_total_ptotal_from_postiton, get_position_by_page
from stucrs.model import create_RecruiterCompany, get_total_ptotal_from_RecruiterCompany, get_company_by_page, \
    create_RecruiterHr, search_hr_id_by_company_id,create_RecruitmentPosition,filter_from_model_by_kw,RecruiterCompany,RecruiterHr


# 转移公司数据
def move_spydercompany_to_company():
    total, pagetotal = get_total_ptotal_from_spyderCompany(500)
    n = 0
    for i in range(1, pagetotal+1):
        get_company_list = get_spyder_company_by_page(i, 500, pagetotal)
        for company in get_company_list:
            if filter_from_model_by_kw(RecruiterCompany, company_id=company.company_id):
                n += 1
                continue
            company_info = {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "company_industry": company.company_industry,
                "address": company.address,
                "company_profile": company.company_profile,
                "company_pic": company.company_pic
            }
            create_RecruiterCompany(company_info)
            n += 1
            print(n)

# move_spydercompany_to_company()

# 创建公司HR
def create_move_spydercompany_to_company():
    total, pagetotal = get_total_ptotal_from_RecruiterCompany(500)
    n = 0
    for i in range(1, pagetotal+1):
        get_company_list = get_company_by_page(i, 500, pagetotal)
        add_list = []
        for company in get_company_list:
            if filter_from_model_by_kw(RecruiterHr, company_id=company.company_id):
                n += 1
                continue
            hr_info = {
                "company_id": company.company_id,
                "name": None if not company.company_name else (company.company_name[0:3] + "Hr") if len(company.company_name) > 3 else (company.company_name + "Hr"),
                "real_name": None if not company.company_name else (company.company_name[0:3] + "Hr") if len(company.company_name) > 3 else (company.company_name + "Hr")
            }
            add_list.append(hr_info)
            n += 1
            print(n)
        create_RecruiterHr(add_list)


# create_move_spydercompany_to_company()

import datetime
# 转移职位数据
def move_spyderposition_to_position():
    total, pagetotal = get_total_ptotal_from_postiton(500)
    n = 0
    for i in range(1, pagetotal+1):
        get_job_list = get_position_by_page(i, 500, pagetotal)
        add_list = []
        for job in get_job_list:
            # 找到company的hrid
            hr = search_hr_id_by_company_id(job.company_id)
            if not hr:
                n+=1
                continue
            job_info = {
                "company_id": job.company_id,
                "hr_id": hr.hr_id,
                "job_title": job.job_title,
                "work_province": job.work_province,
                "work_city": job.work_city,
                "work_address": job.work_address,
                "education_requirements": job.education_requirements,
                "salary_range": job.salary_range,
                "job_description": job.job_description,
                "create_time": datetime.datetime.strptime("2020-"+job.job_puttime+" 00:00:00", "%Y-%m-%d %H:%M:%S")
            }
            # create_RecruitmentPosition(job_info)
            add_list.append(job_info)
            n += 1
            print(n)
        create_RecruitmentPosition(add_list)

move_spyderposition_to_position()