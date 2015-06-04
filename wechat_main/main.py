#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 用于接收微信的消息 '

__author__ = 'Lushen Liao'

import tornado.ioloop
import tornado.web
import hashlib
import xml.etree.ElementTree as ET
import menuEvent.dkfExpertHelp as dEH



def checksignature(signature, timestamp, nonce):
  args = []
  args.append('HealthCommunity')
  args.append(timestamp)
  args.append(nonce)
  args.sort()
  mysig = hashlib.sha1(''.join(args)).hexdigest()
  return mysig == signature


class MainHandler(tornado.web.RequestHandler):

  ####################验证时用#######################
  def get(self):
    signature = self.get_argument('signature')
    timestamp = self.get_argument('timestamp')
    nonce = self.get_argument('nonce')
    echostr = self.get_argument('echostr')
    if checksignature(signature, timestamp, nonce):
      self.write(echostr)
    else:
      self.write('fail')

    ################接收和发送消息##################
  def post(self):
    body = self.request.body
    data = ET.fromstring(body)

    if data.find('MsgType').text == "event": # 发送的消息是event类型
      if data.find('Event').text == "CLICK": # 点击菜单拉取消息时的事件推送
        if data.find('EventKey').text == "expertHelp": #点击的是“专家帮忙”按钮
          self.write(dEH.connectReply(data))
    if data.find('MsgType').text == "text":
      if data.find('Content').text == "请求专家帮助":
        self.write(dEH.connectExport(data))

application = tornado.web.Application([
  (r"/", MainHandler),
])

if __name__ == "__main__":
  application.listen(80)
  tornado.ioloop.IOLoop.instance().start()
