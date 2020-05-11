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
        return dRet(200, "注册成功")
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

