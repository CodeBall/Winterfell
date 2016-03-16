#!/usr/bin/env python
# encoding: utf-8

from app.models import User
from flask.ext.restful import Resource
from flask import jsonify,request
from app import auth,api
import md5


class userLogin(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        m1 = md5.new()
        m1.update(password)
        password = m1.hexdigest()

        user = User.query.filter_by(user_email = username).first()
        if not user or not user.verify_password(password):
            return False
        token = user.generate_auth_token(3600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600,'user_id':user.user_id})


api.add_resource(userLogin,'/users/login')
