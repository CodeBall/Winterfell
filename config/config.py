#!/usr/bin/env python
# encoding: utf-8

import os

class Config:

    @staticmethod
    def init_app(app):
        pass

class development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://%s:%s@%s/%s'%(
        os.environ.get('DATABASE_USERNAME','root'),
        os.environ.get('DATABASE_PASSWORD','BIG BEN'),
        os.environ.get('DATABASE_HOST','localhost'),
        os.environ.get('DATABASE_DB','Winterfell'),
    )

config = {'default':development}
