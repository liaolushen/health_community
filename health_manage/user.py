#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import hashlib

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

class User(object):
    """docstring for User"""
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]

    def verifyUser(self, email, password):
        """
        Args:
            email
            password

        Return:
            If verify successed, return the id of user, the type of id is bson.objectid.ObjectId.
            Else if failed, return the fail reason
        """
        coll = self.db.user
        detail = coll.find_one({"email":email})
        if detail:
            if detail["password"] == md5(password):
                return detail["_id"]
            else:
                return "密码错误！"
        else:
            return "用户名不存在！"

    def addUser(self, email,password):
        """
        Args:
            email
            password

        Return:
            If add successed, return the id of user, the type of id is bson.objectid.ObjectId.
            Else if failed, return the fail reason
        """
        if email != None or password != None:
            coll = self.db.user
            if coll.find_one({"email":email}):
                return "用户名已存在！"
            else:
                new_user = {"email":email, "password":md5(password), "info":[]}
                result = coll.insert_one(new_user)
                return result.insert_id
        else:
            return "输入有问题！"

    def getUserInfo(self, user_id):
        """
        Args:
            user_id

        Return:
            return a list of user info
        """
        coll = self.db.user
        return coll.find_one({"_id":ObjectId(user_id)})["info"]

    def updateUserInfo(self, user_id, user_info):
        """
        Args:
            user_id
            user_info: a dict content user's info

        Return:
            return a string discribe if successed
        """
        coll = self.db.user
        result = coll.update_one({"_id":ObjectId(user_id)}, {'$set': {'info': user_info}})
        if result.matched_count > 0:
            return "保存成功"
        else:
            return "保存失败"

if __name__ == '__main__':
    user = User()
    test = {}
    test['name'] = "test"
    user.updateUserInfo("55ce8475f965b50a21c2e3cd", test)