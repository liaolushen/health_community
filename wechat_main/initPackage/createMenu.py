#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get Create Menu '

__author__ = 'Lushen Liao'

import urllib
import urllib2
from urllib import urlencode
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
from AccessToken import getAccessToken

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + getAccessToken()

menu = '''{
     "button":[
       {
           "name":"社区资讯",
           "sub_button":
           [{
               "type":"click",
               "name":"社区资讯",
               "key":"community_info"
            },
            {
               "type":"click",
               "name":"健康知识",
               "key":"health_knowlege"
            }]
       },
       {
           "name":"医民互动",
           "sub_button":
           [{
               "type":"view",
               "name":"骨质疏松",
               "url":"http://mp.weixin.qq.com/s?__biz=MzA5ODc5NDM2NA==&mid=400252841&idx=1&sn=0f99814ddbfa14d84669fa1f30c70fcd#rd"
            },
            {
               "type":"click",
               "name":"东园新村活动",
               "key":"current_activity"
            }]
      },
      {
           "name":"健康管理",
           "sub_button":
           [{
               "type":"view",
               "name":"白内障诊疗查询",
               "url":"http://45.63.123.71:8100/eyes/"
            },
            {
               "type":"view",
               "name":"医生预约",
               "url":"http://45.63.123.71:8100/doctor/"
            },
            {
               "type":"view",
               "name":"健康记录",
               "url":"http://45.63.123.71:8100/"
            },
            {
               "type":"view",
               "name":"我的药品",
               "url":"http://45.63.123.71:8000/"
            }]
       }]
 }'''

def createMenu():
    request = urllib2.urlopen(posturl, menu.encode('utf-8'))
    return request.read()

if __name__ == '__main__':
    print createMenu()
