#!/usr/bin/env python
# -*- coding: utf-8 -*-

' wechat developer authentic '

__author__ = 'Lushen Liao'

import tornado.ioloop
import tornado.web
import hashlib


def checksignature(signature, timestamp, nonce):
  args = []
  args.append('HealthCommunity')
  args.append(timestamp)
  args.append(nonce)
  args.sort()
  mysig = hashlib.sha1(''.join(args)).hexdigest()
  return mysig == signature


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    signature = self.get_argument('signature')
    timestamp = self.get_argument('timestamp')
    nonce = self.get_argument('nonce')
    echostr = self.get_argument('echostr')
    if checksignature(signature, timestamp, nonce):
      self.write(echostr)
    else:
      self.write('fail')


application = tornado.web.Application([
  (r"/", MainHandler),
])

if __name__ == "__main__":
  application.listen(80)
  tornado.ioloop.IOLoop.instance().start()
