#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from urllib import urlencode
import StringIO
from PIL import Image
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
from initPackage.AccessToken import getAccessToken

addurl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=" + getAccessToken()

def test(postData):
    response = urllib2.urlopen(addurl, json.dumps(postData))
    img = response.read();
    im = Image.open(StringIO.StringIO(img))
    im.save("static/images/"+ postData['media_id'] +"."+im.format, im.format)
    return im.format

if __name__ == '__main__':
    getImage = {"media_id": "1108308918594"};
    print test(getImage)