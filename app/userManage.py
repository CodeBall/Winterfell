#!/usr/bin/env python
# encoding: utf-8
from app import db
from app import User

#查找最大ID
def get_max_id():
    user = User.query.order_by(User.user_id.desc()).first()
    return user.user_id

#根据id查找用户信息
def get_user_by_id(userId):
    user = User.query.filter_by(user_id=userId).first()
    return user

#根据邮箱查询用户信息
del get_user_by_email(userEmail):
    user = User.query.filter_by(user_email=userEmail).first()
    return user


#添加用户信息
def add_user(userinfo):
    #获取添加数据之前的id
    id1 = get_maxc_id()
    user = User()

    user.user_name = userinfo['userName']
    user.user_nikename = userinfo['userNikename']
    user.user_email = userinfo['userEmail']
    user.user_pass = userinfo['userPass']

    #数据持久化
    db.session.add(user)
    db.session.commit()

    #获取添加数据之后的id
    id2 = get_max_id()
    #判断是否添加成功
    if(id1 + 1 == id2):
        return "用户申请成功"
    else:
        return "用户申请失败,请重试"

#删除用户信息
def delete_user(userId):
    #获取该id下的所有单词信息,进行删除操作,未完待续

    #删除用户信息
    User.query.filter_by(user_id = userId).delete()
    db.session.commit()

#修改用户信息
def change_user(userinfo):
    #根据id找到该用户的信息
    user = get_user_by_id(userinfo.user_id)
    #更新用户信息
    user.user_name = userinfo.user_name
    user.user_nikename = userinfo.user_nikename
    user.user_email = userinfo.user_email
    user.user_pass = userinfo.user_pass

    #数据持久化
    db.session.commit()
    return "用户信息更改成功"



