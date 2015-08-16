#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient

class UserInfo(object):
    """docstring for UserInfo"""
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]

    def getInfo():
        pass

    def updateInfo():
        pass

    def createImg():
        pass
