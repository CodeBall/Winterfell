#!/usr/bin/env python
# encoding: utf-8

from app import db
import md5
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

secret_key = 'the quick brown fox jumps over the lazy dog'
class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),nullable=False)
    user_nikename = db.Column(db.String(64),nullable=False)
    user_email=db.Column(db.String(64),nullable=False)
    user_pass=db.Column(db.String(64),nullable=False)

    #repr函数是确定返回class值的
    def __repr__(self):
        return "user's name is %s,email is %s,nikename is %s"%(self.user_name,self.user_email,self.user_nikename)

    #自定义转成json格式函数
    def toJson(self):
        return{
            'id':self.user_id,
            'userName':self.user_name,
            'userNikename':self.user_nikename,
            'user_email':self.user_email,
        }
    #生成密码散列
    def hash_password(self,password):
        m1 = md5.new()
        m1.update(password)
        return m1.hexdigest()

    #验证密码
    def verify_password(self,password):
        if self.user_pass == password:
            return True
        else:
            return False

    #生成token并绑定user_id
    def generate_auth_token(self,expiration=3600):
        s = Serializer(secret_key,expires_in = expiration)
        return s.dumps({'user_id':self.user_id})


    #验证token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['user_id'])
        return user

