#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 16:38
# Author  : W 
# FileName: spyder51Job.py

import requests
import re
from pyquery import PyQuery as pq
from stucrs.model.spyder_model import insertSearchMain, get_total_ptotal_from_searchmain, get_search_main_by_page, search_or_create_spydercompany, add_spyderCompany, search_job_from_spydercompany, \
    update_spyderSearchMain_company_jobinfo_id, add_spyderRecruitmentPosition, get_total_ptotal_from_postiton, get_position_by_page, Session, spyderRecruitmentPosition
import traceback

# 爬取51 job 首层职位搜索信息入库
def Spyder51Job(page=True):
    url = "https://search.51job.com/list/040000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    # 深圳地区url
    # url = "https://search.51job.com/list/040000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "search.51job.com",
        "Referer": "https://search.51job.com/list/080200,000000,0000,01%252C38%252C31%252C32%252C39,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    responselist = []
    for i in range(1000,2001):
        responselist = []
        print("第%s页" % str(i))

        url = "https://search.51job.com/list/040000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        url = url.replace(re.findall(",\d\.html?",url)[0],",%s.html?" % str(i))
        res = requests.get(url, headers=headers)
        res.encoding = res.apparent_encoding
        response = res.text
        doc = pq(response)
        doc("#resultList").children(".el.title").remove()
        resultlist = doc("#resultList").children(".el").items()
        for item in resultlist:
            temdict = {}
            temdict["job_name"] = item.children("p").text()
            company_i = item.children("span:nth-child(2)").children("a")
            temdict["company_name"] = company_i.attr("title")
            temdict["company_link"] = company_i.attr("href")
            temdict["work_place"] = item.children("span:nth-child(3)").text()
            temdict["salary"] = item.children("span:nth-child(4)").text()
            temdict["puttime"] = item.children("span:nth-child(5)").text()
            temdict["job_link"] = item.children("p").children("span a").attr("href")
            # 数据过滤
            if temdict["work_place"] == "异地招聘" or not temdict["salary"]:
                continue
            responselist.append(temdict)
        print("获得%s条数据" % len(responselist))
        # 存入数据库
        insertSearchMain(responselist)
    return responselist

# 根据首层搜索职位信息继续获取公司信息入库
def spyder51CompanyInsertDB():
    # 获取首层职位信息
    total, pagetotal = get_total_ptotal_from_searchmain(500)
    for i in range(1, pagetotal+1):
        n = 0
        page_job_list = get_search_main_by_page(i, 500, pagetotal)
        for job in page_job_list:# 获取单页数据
            n += 1
            print("第%s页 第%s条 总%s页 已处理%s" % (str(i), str(n), str(pagetotal), str((i-1)*500+n-1)))
            if not job.company_id:
                # 查询是否有该公司,有则返回id
                ret_company_id = search_or_create_spydercompany(job)
                if ret_company_id:
                    # 更新job company_id
                    job.company_id = ret_company_id
                    update_spyderSearchMain_company_jobinfo_id(job, "company_id")
                    continue
                if ret_company_id == 0:
                    # 爬取公司信息入库
                    company_info_dict = spyder51CompanyMain(job)
                    if not company_info_dict:# 异常跳过
                        continue
                    new_company = add_spyderCompany(company_info_dict)
                    if not new_company:# 异常跳过
                        continue
                    # 更新job company_id
                    job.company_id = new_company.company_id
                    update_spyderSearchMain_company_jobinfo_id(job, "company_id")
                # 其他异常不处理

# 爬取公司主程序
def spyder51CompanyMain(job):
    try:
        print("爬取公司")
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "search.51job.com",
            "Referer": "https://search.51job.com/list/080200,000000,0000,01%252C38%252C31%252C32%252C39,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        # res = requests.get("https://jobs.51job.com/all/co1088352.html", headers=headers)
        res = requests.get(job.company_link, headers=headers)
        res.encoding = res.apparent_encoding
        response = res.text
        doc = pq(response)
        tags = doc("div.tHeader.tHCop p.ltype").text().replace(" ", "").split("|")
        con_txt = doc("div.tCompany_full div.con_txt")
        addr = doc("div.tCompany_full").children("div.tBorderTop_box.bmsg p.fp")
        address = None if not addr else None if "公司地址" not in addr.text() else doc("div.tCompany_full").children("div.tBorderTop_box.bmsg p.fp:first-child").text().replace("公司地址：", "")
        web = doc("div.tCompany_full").children("div.tBorderTop_box.bmsg p.fp.tmsg")
        company_web = None if not web else web.text().replace("公司官网：", "")
        company_info = {
            "company_name": doc("div.tHeader.tHCop h1").attr("title"),
            "company_tag": tags[0],
            "company_industry": tags[-1],
            "howmany_people": None if len(tags) < 3 else tags[1],
            "company_hold_name": None if not doc("div.tHeader.tHCop p.blicence") else doc("div.tHeader.tHCop p.blicence").children("span").attr("title").replace("营业执照：", ""),
            "company_link": job.company_link,
            "company_pic": None if not doc("div.tHeader.tHCop img") else doc("div.tHeader.tHCop img").attr("src"),
            "company_profile": None if not con_txt else con_txt.text(),
            "address": address,
            "company_web": company_web
        }
        return company_info
    except:
        print(traceback.format_exc())
        return None

# 根据首层搜索职位信息继续获取职位信息入库
def spyder51JobInfoInsertDB():
    # 获取首层职位信息
    total, pagetotal = get_total_ptotal_from_searchmain(500)
    notdo = 0
    for i in range(1, pagetotal + 1):
        n = 0
        page_job_list = get_search_main_by_page(i, 500, pagetotal)
        for job in page_job_list:  # 获取单页数据
            n += 1
            print("第%s页 第%s条 总%s页 已处理%s 无归属%s" % (str(i), str(n), str(pagetotal), str((i - 1) * 500 + n - 1), str(notdo)))
            if not job.company_id:  # 没有公司id 职位信息无归属，直接跳过
                notdo += 1
                continue
            if not job.jobinfo_id:
                # 查询公司是否有该职位id
                ret_jobinfo_id = search_job_from_spydercompany(job)
                if ret_jobinfo_id:
                    # 更新job jobinfo_id
                    job.jobinfo_id = ret_jobinfo_id
                    update_spyderSearchMain_company_jobinfo_id(job, "jobinfo_id")
                    continue
                if ret_jobinfo_id == 0:
                    # 爬取职位信息入库
                    job_info_dict = spyder51JobInfoMain(job)
                    if not job_info_dict:# 异常跳过
                        continue
                    new_job = add_spyderRecruitmentPosition(job_info_dict)
                    if not new_job:# 异常跳过
                        continue
                    # 更新job jobinfo_id
                    job.jobinfo_id = new_job.job_id
                    update_spyderSearchMain_company_jobinfo_id(job, "jobinfo_id")
                # 其他异常不处理

# 更新职位信息入爬虫库
def update51JobInfoInsertDB():
    total, pagetotal = get_total_ptotal_from_postiton(500)
    for i in range(1, pagetotal+1):
        n = 0
        get_job_list = get_position_by_page(i, 500, pagetotal)
        for job in get_job_list:
            n += 1
            print("第%s页 第%s条 总%s页 已处理%s" % (str(i), str(n), str(pagetotal), str((i - 1) * 500 + n - 1)))
            if job.job_link:
                job_info_dict = spyder51JobInfoMain(job)
                if not job_info_dict:
                    continue
                # 更新职位信息
                session = Session()
                session.query(spyderRecruitmentPosition).filter(spyderRecruitmentPosition.job_id==job.job_id).update(job_info_dict)
                session.commit()
                # session.close()



# 爬取职位信息主程序
def spyder51JobInfoMain(job):
    try:
        print("爬取职位信息")
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "search.51job.com",
            "Referer": "https://search.51job.com/list/080200,000000,0000,01%252C38%252C31%252C32%252C39,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        # res = requests.get("https://jobs.51job.com/shenzhen-ftq/122175941.html?s=01&t=0", headers=headers)
        res = requests.get(job.job_link, headers=headers)
        res.encoding = res.apparent_encoding
        response = res.text
        doc = pq(response)
        tags = doc("div.tHeader.tHjob p.msg.ltype").text().replace(" ", "").split("|")
        box2 = doc("div.tCompany_main").children(".tBorderTop_box:nth-child(2)")
        address = None if box2.children("h2").text() != "联系方式" else box2.children("div p.fp").text().replace("上班地址：", "")
        job_info = {
            # "company_id": job.company_id,
            # "job_title": job.job_name,
            "work_province": "广东",
            # "work_city": job.work_place,
            "work_address": address,
            "work_experience_requirements": get_tags(1, tags),
            "education_requirements": get_tags(2, tags),
            # "salary_range": job.salary,
            "job_description": doc("div.bmsg.job_msg.inbox").text(),
            "job_persion_requirements": get_tags(3, tags),
            # "job_puttime": job.puttime,
            # "job_link": job.job_link
        }
        return job_info
    except:
        print(traceback.format_exc())
        return None

def get_tags(n, tags):
    for tag in tags:
        if n == 1:  # 经验要求
            if "经验" in tag:
                return tag
            continue
        if n == 2: # 学历要求
            if tag in ['高中','大专','本科','研究生','博士','初中及以下','中专']:
                return tag
            continue
        if n == 3: # 招多少人
            if "人" in tag:
                return tag
            continue
    return


if __name__ == '__main__':
    # import pprint
    # Spyder51Job()
    import pprint
    # pprint.pprint(spyder51CompanyMain("111"))
    # spyder51CompanyInsertDB()
    # pprint.pprint(spyder51JobInfoMain("1"))
    # spyder51JobInfoInsertDB()
    # update51JobInfoInsertDB()
    pass