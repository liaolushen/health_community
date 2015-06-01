#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get AccessToken '

__author__ = 'Lushen Liao'

import urllib2
import json

getUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
appid = "wxfb869bb2666de5ad"
appsecret = "3ca4d15d14e2f61cee55e52edb53dd3f"

def getAccessToken():
    url = getUrl % (appid, appsecret)
    res = urllib2.urlopen(url).read()
    decode = json.loads(res)
    return decode['access_token']

if __name__ == '__main__':
    print getAccessToken()