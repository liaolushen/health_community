#!/usr/bin/env python
# -*- coding: utf-8 -*-

' auto reply news by instruction '

__author__ = 'Lushen Liao'

import pymongo
from pymongo import MongoClient
import json
import time

def getNews(data):
    instruction = data.find('Content').text.encode("utf-8")
    unprocessed_news = selectNewsFromDB(instruction)
    if unprocessed_news is not None:
        return processNewsToXML(unprocessed_news, data)

def selectNewsFromDB(instruction):
    conn = MongoClient('localhost', 27017)
    db = conn["wechat_main"]
    coll = db["news_source"]
    if not coll.find_one({'type':instruction}):
        return None
    return coll.find({'type':instruction}).sort([('update_time', pymongo.DESCENDING)])[0]  # return the most recently updated news

def processNewsToXML(unprocessed_news, data):
    itemXml = []
    for news_item in unprocessed_news['content']:
        singleXml = """ 
                <item> 
                    <Title><![CDATA[%s]]></Title> 
                    <Description><![CDATA[%s]]></Description> 
                    <PicUrl><![CDATA[%s]]></PicUrl> 
                    <Url><![CDATA[%s]]></Url> 
                </item> 
                """ % (news_item['title'],
                        news_item['description'], 
                        getImageUrl(news_item['thumb_media_id']), 
                        news_item['url'])
        itemXml.append(singleXml)

    reply = """ 
                        <xml> 
                                <ToUserName><![CDATA[%s]]></ToUserName> 
                                <FromUserName><![CDATA[%s]]></FromUserName> 
                                <CreateTime>%s</CreateTime> 
                                <MsgType><![CDATA[news]]></MsgType> 
                                <ArticleCount>%s</ArticleCount> 
                                <Articles> 
                                        %s
                                </Articles> 
                        </xml> 
                """ % (data.find('FromUserName').text,
                        data.find('ToUserName').text,
                        str(int(time.time())),
                        str(len(unprocessed_news['content'])),
                        " ".join(itemXml))
    return reply

def getImageUrl(media_id):
    conn = MongoClient('localhost', 27017)
    db = conn["wechat_main"]
    coll = db["pic_source"]
    item =  coll.find_one({'media_id':media_id})
    if item:
        return item['url']
    else:
        return coll.find_one()['url']
