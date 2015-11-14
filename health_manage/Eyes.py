#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient

import json

class Eyes(object):
    """docstring for Eyes"""
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]

    def create_order(self, order_info):
        """
        Args:
            order_info: a dict contain id_number, name, sex,
            result, time, location, doctor.

        Return:
            return the result of create
        """

        coll = self.db.eyes
        coll.delete_many({"id_number": order_info["id_number"]})
        if coll.insert_one(order_info):
            return {'code': 200, 'info': 'create success'}
        else:
            return {'code': 500, 'info': 'create failure'}


    def get_order_by_id_number(self, id_number):
        """
        Args:
            id_number

        Return:
            if add success, return the order_info
            else return None
        """
        coll = self.db.eyes
        return coll.find_one({"id_number": id_number})

    def get_all_order(self):
        pass

    def get_order_by_id(self, id):
        pass

    def delete_order_by_id(self, id):
        pass

if __name__ == '__main__':
    eyes = Eyes()
    info = {
                "id_number": "id_number",
                "name": "name",
                "sex": "sex",
                "result": "result",
                "time": "time",
                "location": "location",
                "doctor": "doctor"
    }
    print eyes.get_order_by_id_number("id_numer")