#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 用于接收微信的消息 '

__author__ = 'Lushen Liao'

def connectKf(data):
  touser = data.find('ToUserName').text
  fromuser = data.find('FromUserName').text
  replyMsg = """<xml>
                  <ToUserName><![CDATA[%s]]></ToUserName>
                  <FromUserName><![CDATA[%s]]></FromUserName>
                  <CreateTime>%s</CreateTime>
                  <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                </xml>"""
  return replyMsg % (fromuser, touser,  str(int(time.time()))