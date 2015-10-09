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

    def create_order(self, order_info):
        """
        Args:
            order_info: a dict contain user_id, doctor_id, community, doctor,
                hostipal_card, id_card, name, telephone, time.
        Return:
            a dict contain the code and info
        """
        coll = self.db.order
        new_order = order_info
        new_order['status'] = 0;
        result = coll.insert_one(order_info)
        if result:
            return {'code': 200, 'info': 'create success'}
        else:
            return {'code': 500, 'info': 'create failure'}
        return coll.insert_one(order_info).inserted_id

    def get_all_order_by_user(self, user_id):
        """
        Args:
            user_id

        Return:
            return a dict that contain 3 item of uncomfirmed order, comfirmed order, finished order. like that:
            {
                uncomfirmed_order: [{
                    order_id:
                    name:
                    time:
                }],
                comfirmed_order: [],
                finished_order: []
            }
        """
        coll = self.db.order
        return_data = {
                'uncomfirmed_order': [],
                'comfirmed_order': [],
                'finished_order': []
            }

        result = coll.find({"user_id": user_id})

        if result:
            for item in result:
                if item['status'] == 0:
                    return_data['uncomfirmed_order'].append({
                        'order_id': item['_id'],
                        'name': item['name'],
                        'time': item['time']
                    })
                elif item['status'] == 1:
                    return_data['comfirmed_order'].append({
                        'order_id': item['_id'],
                        'name': item['name'],
                        'time': item['time']
                    })
                else:
                    return_data['finished_order'].append({
                        'order_id': item['_id'],
                        'name': item['name'],
                        'time': item['time']
                    })

        return return_data

    def get_order_by_id(self, order_id):
        coll = self.db.order
        return coll.find_one({"_id": ObjectId(order_id)})





if __name__ == '__main__':
    order = Order()
    print order.get_all_order_by_user("55f261d2f965b517181b33a9")