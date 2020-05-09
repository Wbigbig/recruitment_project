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

# 用户注册操作
def create_applicant_user(u_info):
    session.add(Applicant(**u_info))
    session.commit()
    session.close()
    print("applicant_add", u_info)

class User(UserMixin):
    def __init__(self, login_param):
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
        pwd_hs = self.get_password_hash()

    def get_password_hash(self):
        """
        尝试从数据库获取密码
        :return: 返回None则无对应用户
        """
        try:
            user_ret = session.query(Applicant).filter(or_(Applicant.phone == self.phone, Applicant.email == self.email)).first()
            if not user_ret: return
            return user_ret
        except:
            pass