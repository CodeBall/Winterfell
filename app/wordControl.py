#!/usr/bin/env python
# encoding: utf-8

import pymongo
import config
from flask.ext.restful import Resource
from flask import request
from app import api
from app import collect
from datetime import datetime
import json

#获取所有单词信息
class WordsAll(Resource):
    def get(self,userId):
        words = collect.find({"user_id":userId},{"_id":0})
        rnt = []
        for word in words:
            rnt.append(word)

       # json.dumps(rnt)
        return {
            "status": 200,
            "words": rnt
        }

#获取某一时间段的单词信息
class wordsByTime(Resource):
    def get(self,userId,wordTime):
        words = collect.find({"user_id":userId,"word_time":{"$regex":wordTime}},{"_id":0})
        rnt = []
        for word in words:
            rnt.append(word)

        return {
            "status":200,
            "words":rnt
        }

#获取类似于某一释义的单词信息
class wordsByPara(Resource):
    def get(self,userId,keyWords):
        words = collect.find({'user_id':userId,'paraphrase':{'$regex':keyWords}},{'_id':0})

        rnt = []
        for word in words:
            rnt.append(word)

        return{
            "status":200,
            "words":rnt
        }

#根据原句中的关键词找到单词信息
class wordsByOriginal(Resource):
    def get(self,userId,keyWords):
        words = collect.find({'user_id':userId,'original_sent':{'$regex':keyWords}},{'_id':0})

        rnt = []
        for word in words:
            rnt.append(word)

        return{
            "status":200,
            "words":rnt
        }

#根据造句中的关键词找到单词信息
class wordsByMake(Resource):
    def get(self,userId,keyWords):
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

#修改释义
class putParaphrase(Resource):
    def put(self):
        collect.update({"word_id":request.json['word_id']},{"$set":{"paraphrase":request.json['paraphrase']}})

#修改/添加第一条造句
class putMake1(Resource):
    def put(self):
        collect.update({"word_id":request.json['word_id']},{"$set":{"make_sent1":request.json['make_sent1']}})

#修改/添加第二条造句
class putMake2(Resource):
    def put(self):
        collect.update({"word_id":request.json['word_id']},{"$set":{"make_sent2":request.json["make_sent2"]}})

#修改/添加第三条造句
class putMake3(Resource):
    def put(self):
        collect.update({"word_id":request.json['word_id']},{"$set":{"make_sent3":request.json["make_sent3"]}})


api.add_resource(putParaphrase,'/words/put/paraphrase')
api.add_resource(putMake1,'/words/put/make1')
api.add_resource(putMake2,'/words/put/make2')
api.add_resource(putMake3,'/words/put/make3')

#删除单词信息
class deleteWord(Resource):
    def delete(self,wordId):
        collect.remove({"word_id":wordId})

api.add_resource(deleteWord,'/words/delete/<int:wordId>')

#添加单词信息
class addWord(Resource):
    def post(self):
        count = collect.find_one({"count_id":1},{"_id":0})
        word_id = count['count']+1
        word = request.json
        word["word_id"] = word_id
        word["word_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        collect.insert(word)
        collect.update({"count_id":1},{"$set":{"count":word_id}})

api.add_resource(addWord,'/words/add')
