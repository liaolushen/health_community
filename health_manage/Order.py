#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import hashlib
import json

class Order(object):
    """ docstring for Order """
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]

    # def  create_order(self, )