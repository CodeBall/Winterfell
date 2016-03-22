#/usr/bin/env python
# encoding: utf-8

from flask.ext.restful import Resource
from flask import request,abort,jsonify
from app import api, db,auth
from app.models import User,verify_auth_token

class Users(Resource):
    def get(self,userId):
        user = User.query.filter_by(user_id=userId).first()
        user = user.toJson()
        return user

#    def delete(self,userId):
#        User.query.filter_by(user_id=userId).delete()
#        db.session.commit()


class UserLists(Resource):

    def post(self):
        user = User()
        username = request.json['username']
        nikename = request.json['nikename']
        email = request.json['email']
        password = request.json['password']

        user.user_name = username
        user.user_nikename = nikename
        user.user_email = email
        user.user_pass = password

        db.session.add(user)
        db.session.commit()

        return jsonify({'status':200,'username':username,'nikename':nikename,'email':email})

    def put(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"no this user"})
        user.user_name = request.json['username']
        user.user_nikename = request.json['nikename']
        user.user_email = request.json['email']
        user.user_pass = request.json['password']
        db.session.commit()
        return jsonify({"status":200})
class UserEmail(Resource):
    def get(self,email):
        user = User.query.filter_by(user_email = email).first()
        user = user.toJson()
        return user


api.add_resource(Users,'/users/<int:userId>')
api.add_resource(UserLists,'/users')
api.add_resource(UserEmail,'/userbyemail/<string:email>')
