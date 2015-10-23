#!/usr/bin/env python
# -*- coding: utf-8 -*-

' auto reply when user post a text msg '

__author__ = 'Lushen Liao'

from connectDKF import connectDKF
from getNews import getNews
import xml.etree.ElementTree as ET

# def msgRes(data):
#     instruction = data.find('Content').text.encode("utf-8")
#     if instruction == "廖医生":
#         return connectDKF.connectOrderedDKF(data, '1000@health_community')
#     if instruction == "李药师":
#         return connectDKF.connectOrderedDKF(data, '1003@health_community')
#     if instruction == "请求医生帮助":
#         return connectDKF.connectRandomDKF(data)
#     if instruction in ["政策解读", "疫情公布", "服务通知", "政务新闻", "膳食", "周边", "骨质疏松", "糖尿病",
#     "体检", "肾病"]:
#         return getNews.getNews(data)
#     return ''

def msgRes(data):
    instruction = data.find('Content').text.encode("utf-8")
    if instruction in ["政策解读", "疫情公布", "服务通知", "政务新闻", "膳食", "周边", "骨质疏松", "糖尿病",
    "体检", "肾病"]:
        return getNews.getNews(data)
    return ''