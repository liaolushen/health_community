#!/usr/bin/env python
# -*- coding: utf-8 -*-

' auto reply when user post a text msg '

__author__ = 'Lushen Liao'

import time
import sys
import json
import urllib
import urllib2
import xml.etree.ElementTree as ET
import threading
from urllib import urlencode
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from initPackage.AccessToken import getAccessToken


def msgRes(data):
  if data.find('Content').text.encode("utf-8") == "请求医生帮助":
    return connectDKF(data)
  if data.find('Content').text.encode("utf-8") == "政策解读":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "疫情公布":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "服务通知":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "政务新闻":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "膳食":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "周边":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "骨松":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "糖尿病":
    return getNews(data)
  if data.find('Content').text.encode("utf-8") == "体检":
    return getNews(data)

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
  return ET.tostring(jsonToXML(news_json, data))

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
      if keyword == result['item'][offset - post_info['offset']]['content']['news_item'][0]['title'].encode('utf-8').split('|')[0]:
        res_info = {}
        res_info['media_id'] = result['item'][0]['media_id']
        res_info['update_time'] = result['item'][0]['update_time']
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




# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>12345678</CreateTime>
# <MsgType><![CDATA[news]]></MsgType>
# <ArticleCount>2</ArticleCount>
# <Articles>
# <item>
# <Title><![CDATA[title1]]></Title> 
# <Description><![CDATA[description1]]></Description>
# <PicUrl><![CDATA[picurl]]></PicUrl>
# <Url><![CDATA[url]]></Url>
# </item>
# <item>
# <Title><![CDATA[title]]></Title>
# <Description><![CDATA[description]]></Description>
# <PicUrl><![CDATA[picurl]]></PicUrl>
# <Url><![CDATA[url]]></Url>
# </item>
# </Articles>
# </xml> 

def jsonToXML(news_json, data):
  xml = ET.Element('xml')

  ToUserName = ET.SubElement(xml, 'ToUserName')
  ToUserName.text = "![CDATA[" + data.find('FromUserName').text + "]]"

  FromUserName = ET.SubElement(xml, 'FromUserName')
  FromUserName.text = "![CDATA[" + data.find('ToUserName').text + "]]"

  CreateTime = ET.SubElement(xml, 'CreateTime')
  CreateTime.text = str(int(time.time()))

  MsgType = ET.SubElement(xml, 'MsgType')
  MsgType.text = "![CDATA[news]]"

  ArticleCount = ET.SubElement(xml, 'ArticleCount')
  ArticleCount.text = len(news_json['news_item'])

  Articles = ET.SubElement(xml, 'Articles')

  for news_item in news_json['news_item']:
    item = ET.Element('item')
    Title = ET.SubElement(item, 'Title')
    Title.text = "![CDATA[" + news_item['title'] + "]]"

    Description = ET.SubElement(item, 'Description')
    Description.text = "![CDATA[" + news_item['digest'] + "]]"

    PicUrl = ET.SubElement(item, 'PicUrl')
    PicUrl.text = "![CDATA[" + "https://mmbiz.qlogo.cn/mmbiz/9OCyrGmkRVaqnAviagnR9nCWnrXNPWW7rteMXGOHu1Uc6VzkSNYTxF53IzW8AEricdFO33Qky5ia7591fOz3InB4Q/0?wx_fmt=jpeg" + "]]"

    Url = ET.SubElement(item, 'Url')
    Url.text = "![CDATA[" + news_item['url'] + "]]"

    Articles.extend(item)

  return xml

# def test(media_id):
#   post_url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=" + getAccessToken()
#   post_info = {}
#   post_info['media_id'] = media_id
#   request = urllib2.urlopen(post_url, json.dumps(post_info))
#   return request.read()

if __name__ == "__main__":
  print getNewsJson(getMediaId('服务通知'))['news_item'][0]['thumb_media_id']
