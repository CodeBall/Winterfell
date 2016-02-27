#/usr/bin/env python
# encoding: utf-8

from flask.ext.restful import Resource
from flask import request
from app import api, db
from userManage import *
from app.models import User

class Users(Resource):
    def get(self,userId):
        user = User.query.filter_by(user_id=userId).first()
        user = user.toJson()
        return user
    def delete(self,userId):
        User.query.filter_by(user_id=userId).delete()
        db.session.commit()

    #def put(self,userId):
        #user = User.query.filter_by(user_id=userId).first()
        #user.user_id = userId
        #user.user_name = request.json['username']
        #user.user_nikename = request.json['mikename']
        #user.user_email = request.json['email']
        #user.user_pass = request.json['password']

       # db.session.commit()

class UserLists(Resource):
    def post(self):
        user = User()

        user.user_name = request.json['username']
        user.user_nikename = request.json['nikename']
        user.user_email = request.json['email']
        user.user_pass = request.json['password']

        db.session.add(user)
        db.session.commit()

    def put(self):
        user = User.query.filter_by(user_id=request.json['id']).first()
        user.user_id = request.json['id']
        user.user_name = request.json['username']
        user.user_nikename = request.json['nikename']
        user.user_email = request.json['email']
        user.user_pass = request.json['password']
        db.session.commit()


api.add_resource(Users,'/users/<int:user_id>')
api.add_resource(UserLists,'/users')
