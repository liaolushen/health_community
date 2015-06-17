#!/usr/bin/env python
# -*- coding: utf-8 -*-

' response mune_click event '

__author__ = 'Lushen Liao'

import time

def clickRes(data):
  touser = data.find('ToUserName').text
  fromuser = data.find('FromUserName').text
  replyMsg = """<xml>
                  <ToUserName><![CDATA[%s]]></ToUserName>
                  <FromUserName><![CDATA[%s]]></FromUserName>
                  <CreateTime>%s</CreateTime>
                  <MsgType><![CDATA[text]]></MsgType>
                  <Content><![CDATA[%s]]></Content>
                </xml>"""
  replyContent = resContent(data.find('EventKey').text)
  return replyMsg % (fromuser, touser, str(int(time.time())), replyContent)

def resContent(key):
  if key == 'handy_service':
    return '小康一直关注着你所在社区公共卫生服务情况哦，回复一下关键词查看最新动态~\n政策解读\n疫情公布\n服务通知\n政务新闻'
  if key == 'health_life':
    return '小康在你身边，定期为你推送权威健康小知识，回复以下关键词可查看往期精彩专题哦~\n膳食n周边 \n骨松 \n糖尿病 \n体检 \n肾病'
  if key == 'cheap_info':
    return '最新社区周边优惠正在路上，敬请期待~'
  if key == 'my_doctor':
    return '请输入“请求医生帮助”来联系医生'