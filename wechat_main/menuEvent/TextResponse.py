#!/usr/bin/env python
# -*- coding: utf-8 -*-

' auto reply when user post a text msg '

__author__ = 'Lushen Liao'

import time
import sys
import json
import urllib
import urllib2
import threading
from urllib import urlencode
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from initPackage.AccessToken import getAccessToken
import pymongo
from pymongo import MongoClient


def msgRes(data):
  if data.find('Content').text.encode("utf-8") == "廖医生":
    return connectOrderedDKF(data, '1000@health_community')
  if data.find('Content').text.encode("utf-8") == "李药师":
    return connectOrderedDKF(data, '1003@health_community')
  if data.find('Content').text.encode("utf-8") == "请求医生帮助":
    return connectDKF(data)
  for item in ["政策解读", "疫情公布", "服务通知", "政务新闻", "膳食", "周边", "骨松", "糖尿病",
  "体检", "肾病"]:
    return getNews(data)
  return ''

def connectOrderedDKF(data, KfAccount):
  touser = data.find('ToUserName').text
  fromuser = data.find('FromUserName').text
  replyMsg = """  <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                    <TransInfo>
                      <KfAccount><![CDATA[%s]]></KfAccount>
                    </TransInfo>
                  </xml>"""
  return replyMsg % (fromuser, touser, str(int(time.time())), KfAccount)

def connectDKF(data):
  touser = data.find('ToUserName').text
  fromuser = data.find('FromUserName').text
  replyMsg = """<xml>
                  <ToUserName><![CDATA[%s]]></ToUserName>
                  <FromUserName><![CDATA[%s]]></FromUserName>
                  <CreateTime>%s</CreateTime>
                  <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                </xml>"""
  return replyMsg % (fromuser, touser, str(int(time.time())))

def getNews(data):
  media_id = getMediaId(data.find('Content').text)
  news_json = getNewsJson(media_id)
  a = jsonToXML(news_json, data)
  return a

def getMediaId(keyword):
  post_url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=' + getAccessToken()
  post_info = {}
  offset = 0
  total_count = 20
  res_info_list = []
  post_info1 = {"type":"news","offset":0,"count":5}
  post_info2 = {"type":"news","offset":5,"count":5}
  post_info3 = {"type":"news","offset":10,"count":5}
  post_info4 = {"type":"news","offset":15,"count":5}

  def getInfo(post_info):
    offset = post_info['offset']
    request = urllib2.urlopen(post_url, json.dumps(post_info))
    result = json.loads(request.read())
    while offset - post_info['offset'] < 5:
      if keyword == result['item'][offset - post_info['offset']]['content']['news_item'][0]['title'].split('|')[0]:
        res_info = {}
        res_info['media_id'] = result['item'][offset - post_info['offset']]['media_id']
        res_info['update_time'] = result['item'][offset - post_info['offset']]['update_time']
        res_info_list.append(res_info)
        print 'success'
        return
      print offset
      offset = offset + 1

  # 创建新线程
  thread1 = threading.Thread(target = getInfo, args = (post_info1,))
  thread2 = threading.Thread(target = getInfo, args = (post_info2,))
  thread3 = threading.Thread(target = getInfo, args = (post_info3,))
  thread4 = threading.Thread(target = getInfo, args = (post_info4,))

  # 开启新线程
  thread1.start()
  thread2.start()
  thread3.start()
  thread4.start()

  # 添加线程到线程列表
  threads = []
  threads.append(thread1)
  threads.append(thread2)
  threads.append(thread3)
  threads.append(thread4)

  # 等待所有线程完成
  for t in threads:
    t.join()

  sorted(res_info_list, key = lambda res_info : res_info['update_time'])
  return res_info_list[0]['media_id']

def getNewsJson(media_id):
  post_url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=" + getAccessToken()
  post_info = {}
  post_info['media_id'] = media_id
  request = urllib2.urlopen(post_url, json.dumps(post_info))
  return json.loads(request.read())

def jsonToXML(news_json, data):

  itemXml = []
  for news_item in news_json['news_item']:
    singleXml = """ 
        <item> 
          <Title><![CDATA[%s]]></Title> 
          <Description><![CDATA[%s]]></Description> 
          <PicUrl><![CDATA[%s]]></PicUrl> 
          <Url><![CDATA[%s]]></Url> 
          </item> 
        """ % (news_item['title'], news_item['digest'], 
          getImageUrl(news_item['thumb_media_id']), 
          news_item['url'])
    itemXml.append(singleXml)

  reply = """ 
            <xml> 
                <ToUserName><![CDATA[%s]]></ToUserName> 
                <FromUserName><![CDATA[%s]]></FromUserName> 
                <CreateTime>%s</CreateTime> 
                <MsgType><![CDATA[news]]></MsgType> 
                <ArticleCount>%s</ArticleCount> 
                <Articles> 
                    %s
                </Articles> 
            </xml> 
        """ % (data.find('FromUserName').text, data.find('ToUserName').text,
          str(int(time.time())), str(len(news_json['news_item'])), " ".join(itemXml))
  return reply

def getImageUrl(media_id):
  conn = MongoClient('localhost', 27017)
  db = conn["wechat_main"]
  coll = db["pic_source"]
  item =  coll.find_one({'media_id':media_id})
  if item:
    return item['url']
  else:
    return coll.find_one()['url']

if __name__ == "__main__":
  print getImageUrl(123)

