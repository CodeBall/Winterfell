#!/usr/bin/env python
# encoding: utf-8

import pymongo
import config
from flask.ext.restful import Resource
from flask import request,jsonify
from app import api
from app import collect
from app.models import verify_auth_token
from datetime import datetime

#根据id查询单词
class wordsId(Resource):
    def get(self,wordId):
        words = collect.find({"word_id":wordId},{"_id":0,"user_id":0,"word_time":0})
        rnt = []
        for word in words:
            rnt.append(word)

        if not word:
            return{
                "status":"empty"
            }
        return{
            "status":200,
            "words":word
        }
api.add_resource(wordsId,'/words/<int:wordId>')

#获取所有单词信息
class WordsAll(Resource):
    def get(self,userId,No1,count):
        words = collect.find({"user_id":userId},{"_id":0,"original_sent":0,"word_time":0,"user_id":0,
                                                 "make_sent1":0,"make_sent2":0,"make_sent3":0}).skip(No1).limit(count)
        rnt = []
        for word in words:
            rnt.append(word)

        if not rnt:
            return{
                "status":"empty"
            }
       # json.dumps(rnt)
        return {
            "status": 200,
            "words": rnt
        }
class WordsAllCount(Resource):
    def get(self,userId):
        count = collect.find({"user_id":userId}).count()
        return count
api.add_resource(WordsAll,'/words/<int:userId>/<int:No1>/<int:count>')
api.add_resource(WordsAllCount,'/words/<int:userId>/count')
#获取某一时间段的单词信息
class wordsByTime(Resource):
    def get(self,userId,wordTime,No1,count):
        words = collect.find({"user_id":userId,"word_time":{"$regex":wordTime}},{"_id":0}).skip(No1).limit(count)
        rnt = []
        for word in words:
            rnt.append(word)

        if not rnt:
            return{
                "status":"empty"
            }
        return {
            "status":200,
            "words":rnt
        }

class wordByTimeCount(Resource):
    def get(self,userId,wordTime):
        count = collect.find({"user_id":userId,"word_time":{"$regex":wordTime}}).count()
        return count

api.add_resource(wordByTimeCount,'/words/time/<int:userId>/<string:wordTime>/count')
api.add_resource(wordsByTime,'/words/time/<int:userId>/<string:wordTime>/<int:No1>/<int:count>')

#获取类似于某一释义的单词信息
class wordsByPara(Resource):
    def get(self,userId,keyWords,No1,count):
        words = collect.find({'user_id':userId,'paraphrase':{'$regex':keyWords}},{'_id':0}).skip(No1).limit(count)

        rnt = []
        for word in words:
            rnt.append(word)

        if not rnt:
            return{
                "status":"empty"
            }
        return{
            "status":200,
            "words":rnt
        }
class wordByParaCount(Resource):
    def get(self,userId,keyWords):
        count = collect.find({'user_id':userId,'paraphrase':{'$regex':keyWords}},{'_id':0}).count()
        return count

api.add_resource(wordsByPara,'/words/paraphrase/<int:userId>/<string:keyWords>/<int:No1>/<int:count>')
api.add_resource(wordByParaCount,'/words/paraphrase/<int:userId>/<string:keyWords>/count')

#根据原句中的关键词找到单词信息
class wordsByOriginal(Resource):
    def get(self,userId,keyWords,No1,count):
        words = collect.find({'user_id':userId,'original_sent':{'$regex':keyWords}},{'_id':0}).skip(No1).limit(count)

        rnt = []
        for word in words:
            rnt.append(word)

        if not rnt:
            return{
                "status":"empty"
            }
        return{
            "status":200,
            "words":rnt
        }

class wordsOriginCount(Resource):
    def get(self,userId,keyWords):
        count = collect.find({'user_id':userId,'original_sent':{'$regex':keyWords}},{'_id':0}).count()
        return count
api.add_resource(wordsByOriginal,'/words/original/<int:userId>/<string:keyWords>/<int:No1>/<int:count>')
api.add_resource(wordsOriginCount,'/words/original/<int:userId>/<string:keyWords>/count')


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

        if not rnt:
            return{
                "status":"empty"
            }
        return{
            "status":200,
            "words":rnt
        }
class wordByMakeCount(Resource):
    def get(self,userId,keyWords):
        count = collect.find({'user_id':userId,'make_sent1':{'$regex':keyWords}},{'_id':0}).count()
        count += collect.find({'user_id':userId,'make_sent2':{'$regex':keyWords}},{'_id':0}).count()
        count += collect.find({'user_id':userId,'make_sent3':{'$regex':keyWords}},{'_id':0}).count()
        return count
api.add_resource(wordByMakeCount,'/words/make/<int:userId>/<string:keyWords>/count')
api.add_resource(wordsByMake,'/words/make/<int:userId>/<string:keyWords>')


#修改释义
class putParaphrase(Resource):
    def put(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        id = int(request.json['wordId'])
        collect.update_one({"word_id":id},{"$set":{"paraphrase":request.json['paraphrase']}})
        return{
            "status":200
        }
#修改/添加第一条造句
class putMake1(Resource):
    def put(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        id = int(request.json['wordId'])
        collect.update({"word_id":id},{"$set":{"make_sent1":request.json['makeSent1']}})
        return{
            "status":200
        }

#修改/添加第二条造句
class putMake2(Resource):
    def put(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        id = int(request.json['wordId'])
        collect.update({"word_id":id},{"$set":{"make_sent2":request.json["makeSent2"]}})
        return{
            "status":200
        }

#修改/添加第三条造句
class putMake3(Resource):
    def put(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        id = int(request.json['wordId'])
        collect.update({"word_id":id},{"$set":{"make_sent3":request.json["makeSent3"]}})
        return{
            "status":200
        }


api.add_resource(putParaphrase,'/words/update/paraphrase')
api.add_resource(putMake1,'/words/update/make1')
api.add_resource(putMake2,'/words/update/make2')
api.add_resource(putMake3,'/words/update/make3')

#删除单词信息
class deleteWord(Resource):
    def delete(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        id = int(request.json['wordId'])
        collect.remove({"word_id":id})
        return{
            "status":200
        }

#删除某个单词的某一个内容
class updateWord(Resource):
    def delete(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        wordId = request.json['wordId']
        field = request.json['delete_field']
        value = request.json['delete_value']
        collect.update({"word_id":wordId},{"$unset":{field:value}})
        return{
            "status":200
        }

api.add_resource(deleteWord,'/words/delete')
api.add_resource(updateWord,'/words/update')

#添加单词信息
class addWord(Resource):
    def post(self):
        token = request.json['token']
        user = verify_auth_token(token)
        if user is None:
            return jsonify({"status":"wrong"})
        count = collect.find_one({"count_id":1},{"_id":0})
        word_id = count['count']+1
        word = request.json
        del word['token']
        word["word_id"] = word_id
        word["word_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        collect.insert(word)
        collect.update({"count_id":1},{"$set":{"count":word_id}})
        return{
            "status":200
        }

api.add_resource(addWord,'/words/add')
