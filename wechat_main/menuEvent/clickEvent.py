#!/usr/bin/env python
# -*- coding: utf-8 -*-

' response mune_click event '

__author__ = 'Lushen Liao'

import time

reply_msg = """ 
                <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                </xml>
            """

def subscribe_res(data):
    touser = data.find('ToUserName').text
    fromuser = data.find('FromUserName').text
    reply_content = res_content("subscribe")
    return reply_msg % (fromuser, touser, str(int(time.time())), reply_content)

def click_res(data):
    touser = data.find('ToUserName').text
    fromuser = data.find('FromUserName').text
    reply_content = res_content(data.find('EventKey').text)
    return reply_msg % (fromuser, touser, str(int(time.time())), reply_content)

def res_content(key):
    if key == 'community_info':
        return "社区有咩料。小康都知道～回复以下关键词，看看最近都有那些不能错过的信息吧！\n"\
            + "疫情公布\n"\
            + "服务通知\n"\
            + "政策解读"
    if key == 'health_knowlege':
        return "小康在你身边，定期为你推送权威健康小知识，回复以下关键词可查看往期精彩专题哦~\n"\
            + "骨质疏松\n"\
            + "膳食\n"\
            + "周边\n"\
            + "糖尿病\n"\
            + "体检\n"\
            + "肾病"
    if key == 'subscribe':
        return "感谢您的关注【玫瑰】\n"\
            + "我们是“社区小康”，您身边最贴心的全能健康管家。\n\n"\
            + "点击屏幕下方菜单即可开始健康之旅~\n"\
            + "1.社区资讯\n"\
            + "最新、最权威的医疗资讯、社区福利、政府政策\n"\
            + "2.医民互动\n"\
            + "第一期专题——“骨质疏松”正在进行，省医专家降临东园新村，回复“活动”了解详细信息\n"\
            + "3.健康管理\n"\
            + "家庭医生、健康记录、我的药品正在路上，敬请期待~"
    if key == "current_activity":
        return "中山大学新型社区健康传播项目——“给生活加骨劲”主题活动走进东园新村\n\n"\
            + "时间：10月24日（周六）\n"\
            + "地点：东园新村居委会门前\n"\
            + "流程：\n"\
            + "1.健康检查 9:10—11:00 骨密度监测、血压、血糖检测\n"\
            + "2.社区义诊 9:10—11:30 农林上社区医院专家医生回答居民咨询及分析体检结果\n"\
            + "3.专家讲座 10:10—10:50 题目：骨质疏松症的防治\n"\
            + "主讲：智喜梅\n"\
            + "    广东省人民医院内分泌科副主任医师\n"\
            + "    中华医学会骨质疏松及骨矿盐疾病学分会青年委员\n"\
            + "4.互动游戏 9:10—11:30 健康知识抢答及惊喜礼品"


