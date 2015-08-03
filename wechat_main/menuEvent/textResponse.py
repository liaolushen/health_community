#!/usr/bin/env python
# -*- coding: utf-8 -*-

' auto reply when user post a text msg '

__author__ = 'Lushen Liao'

# import time
# import sys
# import json
# import urllib
# import urllib2
# from urllib import urlencode
# from os import sys, path
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# from initPackage.AccessToken import getAccessToken
# import pymongo
# from pymongo import MongoClient

from connectDKF import connectDKF
from getNews import getNews
import xml.etree.ElementTree as ET

def msgRes(data):
    instruction = data.find('Content').text.encode("utf-8")
    if instruction is "廖医生":
        return connectDKF.connectOrderedDKF(data, '1000@health_community')
    if instruction is "李药师":
        return connectDKF.connectOrderedDKF(data, '1003@health_community')
    if instruction is "请求医生帮助":
        return connectDKF.connectRandomDKF(data)
    if instruction in ["政策解读", "疫情公布", "服务通知", "政务新闻", "膳食", "周边", "骨松", "糖尿病",
    "体检", "肾病"]:
        return getNews.getNews(data)
    return ''

# if __name__ == '__main__':
#     data = """<xml>
#              <ToUserName>hello</ToUserName>
#              <FromUserName>hello</FromUserName> 
#              <CreateTime>1348831860</CreateTime>
#              <MsgType>text</MsgType>
#              <Content>廖医生</Content>
#              <MsgId>1234567890123456</MsgId>
#              </xml>"""
#     data = ET.fromstring(data)
#     print connectDKF.connectOrderedDKF(data, '1003@health_community')
