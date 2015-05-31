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
           "name":"健康资讯",
           "sub_button":
           [{
               "type":"click",
               "name":"便民服务",
               "key":"V1001_ALERT"
            },
            {
               "type":"click",
               "name":"健康生活",
               "key":"V1001_HELP"
            },
            {
               "type":"click",
               "name":"优惠资讯",
               "key":"V1001_CHEAP"
            }]
       },
       {
           "name":"微互动",
           "sub_button":
           [{
               "type":"view",
               "name":"专家帮忙",
                "url":"http://120.25.234.58:8000/"
            },
            {
               "type":"view",
               "name":"线下活动",
               "url":"http://120.25.234.58:8000/"
            }]
      },
      {
           "name":"健康管理",
           "sub_button":
           [{
               "type":"click",
               "name":"健康档案",
               "key":"V1001_SYSTEX"
            },
            {
               "type":"click",
               "name":"我的医生",
               "key":"V1001_huabei"
            },
            {
               "type":"click",
               "name":"我的药师",
               "key":"V1001_huadong"
            },
            {
               "type":"view",
               "name":"我的药品",
               "url":"http://120.25.234.58:8000/"
            }]
       }]
 }'''

def createMenu():
    request = urllib2.urlopen(posturl, menu.encode('utf-8') )
    return request.read()

if __name__ == '__main__':
    print createMenu()
