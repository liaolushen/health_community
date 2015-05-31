#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get AccessToken '

__author__ = 'Lushen Liao'

import urllib2
import json

getUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
appid = "wxac5aef1e95bbecb5"
appsecret = "8562fa3feededc00c898afa4dec61cef"

def getAccessToken():
    url = getUrl % (appid, appsecret)
    res = urllib2.urlopen(url).read()
    decode = json.loads(res)
    return decode['access_token']

if __name__ == '__main__':
    print getAccessToken()