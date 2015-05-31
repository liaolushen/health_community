#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get kfservice '

__author__ = 'Lushen Liao'

import urllib
import urllib2
from urllib import urlencode
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
from AccessToken import getAccessToken

addurl = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token=" + getAccessToken()

kfaccount = '''{
    "kf_account" : "1000@gh_2fe42c1ceb7b",
    "nickname" : "客服0",
    "password" : "123456"
}'''

def create_kf():
    request = urllib2.urlopen(addurl, kfaccount.encode('utf-8') )
    return request.read()

if __name__ == '__main__':
    print create_kf()