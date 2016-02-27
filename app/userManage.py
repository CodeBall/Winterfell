#!/usr/bin/env python
#-*- coding:utf-8 –*-
from app import db
from app.models import User
from flask import request


#根据id查找用户信息
def get_user_by_id(userId):
    user = User.query.filter_by(user_id=userId).first()
    user = user.toJson()
    return user

#根据邮箱查询用户信息
def get_user_by_email(userEmail):
    user = User.query.filter_by(user_email=userEmail).first()
    return user


#添加用户信息
def add_user():
    user = User()

    user.user_name = request.json['userName']
    user.user_nikename = request.json['userNikename']
    user.user_email = request.json['userEmail']
    user.user_pass = request.json['userPass']

    #数据持久化
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        db.session.rollback


#删除用户信息
def delete_user(userId):
    #获取该id下的所有单词信息,进行删除操作,未完待续

    #删除用户信息
    User.query.filter_by(user_id = userId).delete()
    db.session.commit()

#修改用户信息
def change_user():
    #根据id找到该用户的信息
    user = get_user_by_id(request.json["user_id"])
    #更新用户信息
    user.user_name = request.json["user_name"]
    user.user_nikename = request.json['user_nikename']
    user.user_email = request.json['user_email']
    user.user_pass = request.json['user_pass']

    #数据持久化
    db.session.commit()



