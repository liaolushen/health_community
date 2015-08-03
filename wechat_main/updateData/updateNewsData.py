#!/usr/bin/env python
# -*- coding: utf-8 -*-

' update the article datebase automatic '

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
coll = db["news_source"]

def newsUpdate(delay):
    post_url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=" + getAccessToken()

    def update(delay):
        while True:
            total_count = getTotalCount()
            offset = 0
            count = 1
            while offset < total_count:
                post_info = {"type":"news","offset":offset,"count":count}
                request = urllib2.urlopen(post_url, json.dumps(post_info))
                result = json.loads(request.read())
                dbCheck(result)
                offset += count
            time.sleep(delay)

    thread = threading.Thread(target = update, args = (delay,))
    thread.start()
    return

def getTotalCount():
    get_url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=' + getAccessToken()
    res = urllib2.urlopen(get_url).read()
    decode = json.loads(res)
    return decode['news_count']

def dbCheck(data):
    for item in data['item']:
        if not coll.find_one({'media_id':item['media_id']}):
            newsInsert(item)

def newsInsert(item):
    insert_item = {}
    insert_item['media_id'] = item['media_id']
    insert_item['update_time'] = item['update_time']
    insert_item['type'] = item['content']['news_item'][0]['title'].split('|')[0].encode("utf-8")
    content = []
    for news_item in item['content']['news_item']:
        insert_single_item = {}
        insert_single_item['title'] = news_item['title']
        insert_single_item['description'] = news_item['digest']
        insert_single_item['url'] = news_item['url']
        insert_single_item['thumb_media_id'] = news_item['thumb_media_id']
        content.append(insert_single_item)
    insert_item['content'] = content
    coll.insert_one(insert_item)


if __name__ == '__main__':
    newsUpdate(500)