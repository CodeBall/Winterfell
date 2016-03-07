#!/usr/bin/env python
# encoding: utf-8

from app.models import User
from flask.ext.restful import Resource
from flask import jsonify,g
from app import auth,api
import md5

@auth.verify_password
def verify_password(username_or_token,password):
    m1 = md5.new()
    m1.update(password)
    password = m1.hexdigest()

    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(user_email = username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True

class userLogin(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(3600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600,'user_id':g.user.user_id})


api.add_resource(userLogin,'/users/login')
