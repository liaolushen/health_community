#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 用于接收微信的消息 '

__author__ = 'Lushen Liao'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import hashlib
import xml.etree.ElementTree as ET
import menuEvent.clickEvent as CE
import menuEvent.textResponse as TR
from updateData import updateData

import os

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

def checksignature(signature, timestamp, nonce):
  args = []
  args.append('HealthCommunity')
  args.append(timestamp)
  args.append(nonce)
  args.sort()
  mysig = hashlib.sha1(''.join(args)).hexdigest()
  return mysig == signature

class Application(tornado.web.Application):
  def __init__(self):
    settings = dict (
      handlers=[(r'/', MainHandler), (r'/image/(.*)', ImageHandler)],
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      debug=True
    )
    tornado.web.Application.__init__(self, **settings)


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
        self.write(CE.clickRes(data))
    if data.find('MsgType').text == "text":
      self.write(TR.msgRes(data))

class ImageHandler(tornado.web.RequestHandler):
  """get image"""
  def get(self, *args):
    img_id = args[0]
    img_name = "default.JPEG"
    for root, dirs, files in os.walk('static/images/'):
      for file_name in files:
        if img_id in file_name:
          img_name = file_name
          break

    self.write('<input type="image" src="%s" />' %
      self.static_url("images/" + img_name))


if __name__ == "__main__":
  #create a thread update pic datebase once a hour
  updateData.updateAllData(3600)

  tornado.options.parse_command_line()
  HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
  HTTP_SERVER.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
