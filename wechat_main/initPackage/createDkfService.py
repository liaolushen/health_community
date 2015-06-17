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

#对字符串进行MD5加密
def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()


def create_kf(kfaccount):
    request = urllib2.urlopen(addurl, kfaccount.encode('utf-8') )
    return request.read()

kfaccount = json.dumps({"kf_account" : "1000@health_community"
                       ,"nickname" : "客服MM"
                       ,"password" : md5("123456")});


if __name__ == '__main__':
    print create_kf(kfaccount)