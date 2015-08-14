#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient

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
        coll = self.db.user
        detail = coll.find_one({"email":email})
        if detail:
            if detail["password"] == md5(password):
                return None
            else:
                return "密码错误！"
        else:
            return "用户名不存在！"

    def addUser(self, email,password):
        if email != None or password != None:
            coll = self.db.user
            if coll.find_one({"email":email}):
                return "用户名已存在！"
            else:
                new_user = {"email":email, "password":md5(password)}
                coll.insert_one(new_user)
                return None
        else:
            return "输入有问题！"

if __name__ == '__main__':
    user = User()
    print user.verifyUser("admin@admin.com", "admin")