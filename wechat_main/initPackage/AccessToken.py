#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get AccessToken '

__author__ = 'Lushen Liao'

import urllib2
import json
import time

getUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
appid = "wxfb869bb2666de5ad"
appsecret = "3ca4d15d14e2f61cee55e52edb53dd3f"

def getAccessToken():
    f = open('data/AccessToken.json', 'r')
    f_content = json.loads(f.read())
    f.close()
    if time.time() - f_content['create_time'] > 7000:
        updateAccessToken()
        with open('data/AccessToken.json', 'r') as f:
            return json.loads(f.read())['access_token']
    return f_content['access_token']


def updateAccessToken():
    url = getUrl % (appid, appsecret)
    res = urllib2.urlopen(url).read()
    decode = json.loads(res)
    update_content = {}
    update_content['access_token'] = decode['access_token']
    update_content['create_time'] = time.time()
    update_content = json.dumps(update_content)
    with open('data/AccessToken.json', 'w') as f:
        f.write(update_content)

if __name__ == '__main__':
    print getAccessToken()