#!/usr/bin/env python
# encoding: utf-8

import pymongo
import config
from flask.ext.restful import Resource
from flask import request
from app import api
import json

class WordsAll(Resource):
    def get(self,userId):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]
        words = collect.find({"user_id":userId},{"_id":0})
        rnt = []
        for word in words:
            rnt.append(word)

       # json.dumps(rnt)
        return {
            "status": 200,
            "words": rnt
        }

class wordsByTime(Resource):
    def get(self,userId,wordTime):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]
        words = collect.find({"user_id":userId,"word_time":{"$regex":wordTime}},{"_id":0})
        rnt = []
        for word in words:
            rnt.append(word)

        return {
            "status":200,
            "words":rnt
        }

class wordsByPara(Resource):
    def get(self,userId,keyWords):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]
        words = collect.find({'user_id':userId,'paraphrase':{'$regex':keyWords}},{'_id':0})

        rnt = []
        for word in words:
            rnt.append(word)

        return{
            "status":200,
            "words":rnt
        }

class wordsByOriginal(Resource):
    def get(self,userId,keyWords):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]
        words = collect.find({'user_id':userId,'original_sent':{'$regex':keyWords}},{'_id':0})

        rnt = []
        for word in words:
            rnt.append(word)

        return{
            "status":200,
            "words":rnt
        }

class wordsByMake(Resource):
    def get(self,userId,keyWords):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]
        words = collect.find({'user_id':userId,'make_sent1':{'$regex':keyWords}},{'_id':0})
        rnt = []
        for word in words:
            rnt.append(word)

        words = collect.find({'user_id':userId,'make_sent2':{'$regex':keyWords}},{'_id':0})
        for word in words:
            rnt.append(word)

        words = collect.find({'user_id':userId,'make_sent3':{'$regex':keyWords}},{'_id':0})
        for word in words:
            rnt.append(word)

        return{
            "status":200,
            "words":rnt
        }

api.add_resource(WordsAll,'/words/<int:userId>')
api.add_resource(wordsByTime,'/words/time/<int:userId>/<string:wordTime>')
api.add_resource(wordsByPara,'/words/paraphrase/<int:userId>/<string:keyWords>')
api.add_resource(wordsByOriginal,'/words/original/<int:userId>/<string:keyWords>')
api.add_resource(wordsByMake,'/words/make/<int:userId>/<string:keyWords>')

class putParaphrase(Resource):
    def put(self):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        collect = db[config.MONGO_COLL]

        wordId = request.json['word_id']

        return collect.update({"word_id":wordId},{"$set":{"paraphrase":request.json['paraphrase']}})


api.add_resource(putParaphrase,'/words/put/paraphrase')

