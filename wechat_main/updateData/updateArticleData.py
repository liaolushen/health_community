#!/usr/bin/env python
# -*- coding: utf-8 -*-

' update the pic datebase automatic '

__author__ = 'Lushen Liao'

import urllib2
import json
import time
import threading

import pymongo
from pymongo import MongoClient
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from initPackage.AccessToken import getAccessToken

conn = MongoClient('localhost', 27017)
db = conn["wechat_main"]
coll = db["pic_source"]

def PicUpdate(delay):
  post_url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=" + getAccessToken()

  def update(delay):
    while True:
      total_count = getTotalCount()
      offset = 0
      while offset < total_count:
        post_info = {"type":"image","offset":offset,"count":20}
        request = urllib2.urlopen(post_url, json.dumps(post_info))
        result = json.loads(request.read())
        dbCheck(result)
        offset += 20
      print "time1"
      time.sleep(delay)

  thread = threading.Thread(target = update, args = (delay,))
  thread.start()
  return

def getTotalCount():
  get_url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=' + getAccessToken()
  res = urllib2.urlopen(get_url).read()
  decode = json.loads(res)
  return decode['image_count']

def dbCheck(data):
  for item in data['item']:
    if not coll.find_one({'media_id':item['media_id']}):
      coll.insert_one({'media_id':item['media_id'], 'url':item['url']})

if __name__ == '__main__':
  PicUpdate(5)