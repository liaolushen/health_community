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
        return '小康在你身边，定期为你推送权威健康小知识，回复以下关键词可查看往期精彩专题哦~\n膳食\n周边\n骨松\n糖尿病\n体检\n肾病'
    if key == 'cheap_info':
        return '最新社区周边优惠正在路上，敬请期待~'
    if key == 'my_doctor':
        return '小康在你身边，专业医生随时与你沟通。现在的值班医生是廖医生，输入"廖医生"即可与廖医生进行实时对话~'
    if key == 'my_pharmacist':
        return '小康在你身边，专业药师随时与你沟通。现在的值班药师是李药师，输入"李药师"即可与李药师进行实时对话~'
