#!/usr/bin/env python
# -*- coding: utf-8 -*-

' connect dkf system'

__author__ = 'Lushen Liao'

import time

def connectOrderedDKF(data, KfAccount):
    touser = data.find('ToUserName').text
    fromuser = data.find('FromUserName').text
    replyMsg = """  <xml>
                                    <ToUserName><![CDATA[%s]]></ToUserName>
                                    <FromUserName><![CDATA[%s]]></FromUserName>
                                    <CreateTime>%s</CreateTime>
                                    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                                    <TransInfo>
                                        <KfAccount><![CDATA[%s]]></KfAccount>
                                    </TransInfo>
                             </xml>"""
    return replyMsg % (fromuser, touser, str(int(time.time())), KfAccount)

def connectRandomDKF(data):
    touser = data.find('ToUserName').text
    fromuser = data.find('FromUserName').text
    replyMsg = """<xml>
                                <ToUserName><![CDATA[%s]]></ToUserName>
                                <FromUserName><![CDATA[%s]]></FromUserName>
                                <CreateTime>%s</CreateTime>
                                <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                          </xml>"""
    return replyMsg % (fromuser, touser, str(int(time.time())))