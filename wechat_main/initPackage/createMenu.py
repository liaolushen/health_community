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
               "key":"handy_service"
            },
            {
               "type":"click",
               "name":"健康生活",
               "key":"health_life"
            },
            {
               "type":"click",
               "name":"优惠资讯",
               "key":"cheap_info"
            }]
       },
       {
           "name":"微互动",
           "sub_button":
           [{
               "type":"click",
               "name":"专家帮忙",
               "key":"expert_help"
            },
            {
               "type":"view",
               "name":"线下活动",
               "url":"http://www.sojump.com/jq/5287934.aspx"
            }]
      },
      {
           "name":"健康管理",
           "sub_button":
           [{
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
