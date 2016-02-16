#!/usr/bin/env python
# encoding: utf-8

from app import db

class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),nullable=False)
    user_nikename = db.Column(db.String(64),nullable=False)
    user_email=db.Column(db.String(64),nullable=False)
    user_pass=db.Column(db.String(64),nullable=False)

    def __init__(self,name,nikename,email,Pass):
        self.user_name=name
        self.user_nikename=nikename
        self.user_email=email
        self.user_pass=Pass

    '''repr函数是确定返回class值的'''
    def __repr__(self):
        return "user's name is %s,email is %s,nikename is %s"%(self.user_name,self.user_email,self.user_nikename)

    '''自定义转成json格式函数'''
    def toJson(self):
        return{
            'id':self.user_id,
            'userName':self.user_name,
            'userNikename':self.user_nikename,
            'user_email':self.user_email,
        }
