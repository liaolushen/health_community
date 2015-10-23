#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get AccessToken '

__author__ = 'Lushen Liao'

import urllib2
import json
import time

import pymongo
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn["wechat_main"]
coll = db["access_token"]

getUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
appid = "wxfb869bb2666de5ad"
appsecret = "3ca4d15d14e2f61cee55e52edb53dd3f"

def getAccessToken():
    db_content = coll.find_one()
    if time.time() - db_content['create_time'] > 3000:
        updateAccessToken()
        db_content = coll.find_one()
    return db_content['access_token']


def updateAccessToken():
    old_content = coll.find_one()
    url = getUrl % (appid, appsecret)
    res = urllib2.urlopen(url).read()
    decode = json.loads(res)
    coll.replace_one({'access_token':old_content['access_token'], 'create_time':old_content['create_time']},
        {'access_token':decode['access_token'], 'create_time':time.time()})

if __name__ == '__main__':
    print getAccessToken()