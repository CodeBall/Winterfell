#/usr/bin/env python
# encoding: utf-8

from flask.ext.restful import Resource
from flask import request,abort,jsonify
from app import api, db
from app.models import User

class Users(Resource):
    def get(self,userId):
        user = User.query.filter_by(user_id=userId).first()
        user = user.toJson()
        return user
    def delete(self,userId):
        User.query.filter_by(user_id=userId).delete()
        db.session.commit()


class UserLists(Resource):
    def post(self):
        user = User()
        username = request.json['username']
        nikename = request.json['nikename']
        email = request.json['email']
        password = request.json['password']

        if username is None or nikename is None or nikename is None or email is None or password is None:
            abort(400)

        user.user_name = username
        user.user_nikename = nikename
        user.user_email = email
        user.user_pass = user.hash_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'username':username,'nikename':nikename,'email':email})

    def put(self):
        user = User.query.filter_by(user_id=request.json['id']).first()
        user.user_id = request.json['id']
        user.user_name = request.json['username']
        user.user_nikename = request.json['nikename']
        user.user_email = request.json['email']
        user.user_pass = request.json['password']
        db.session.commit()
class UserEmail(Resource):
   def get(self,email):
        user = User.query.filter_by(user_email = email).first()
        user = user.toJson()
        return user


api.add_resource(Users,'/users/<int:userId>')
api.add_resource(UserLists,'/users')
api.add_resource(UserEmail,'/userbyemail/<string:email>')
