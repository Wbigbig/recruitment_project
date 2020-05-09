#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/5/9 16:14
# Author  : W
# FileName: __init__.py.py
"""
增删改查，执行数据操作
"""

from .model_table import *

# 用户注册操作
def create_applicant_user(u_info):
    session.add(Applicant(**u_info))
    session.commit()
    session.close()
    print("applicant_add", u_info)

u_info = {
    "user_name": "开朝元老",
    "phone": "00000000000",
    "password": "11111111111"
}

create_applicant_user(u_info)





