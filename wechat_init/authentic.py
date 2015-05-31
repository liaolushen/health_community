#!/usr/bin/env python
# -*- coding: utf-8 -*-

' wechat developer authentic '

__author__ = 'Lushen Liao'

import time
from flask import Flask,request, make_response
import hashlib

app = Flask(__name__)
app.debug = True
 
@app.route('/', methods = ['GET'] )
def wechat_auth():
  token = 'liaolushen'
  query = request.args
  signature = query.get('signature', '')
  timestamp = query.get('timestamp', '')
  nonce = query.get('nonce', '')
  echostr = query.get('echostr', '')
  s = [timestamp, nonce, token]
  s.sort()
  s = ''.join(s)
  if ( hashlib.sha1(s).hexdigest() == signature ):
    return make_response(echostr)

if __name__ == '__main__':
  app.run(post='0.0.0.0', port=80)
