#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import hashlib
import json

class User(object):
    """docstring for User"""
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]
        self.attr_list = ["name", "sex", "birth_date", "birth_locate", "job", "education", "blood", "RH", "marry", "history"]

    def __md5(self, str):
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()

    def verify_user(self, email, password):
        """
        Args:
            email
            password

        Return:
            If verify successed, return the id of user, the type of id is bson.objectid.ObjectId.
            Else if failed, return the fail reason
        """
        coll = self.db.user
        detail = coll.find_one({"email":email})
        if detail:
            if detail["password"] == self.__md5(password):
                return detail["_id"]
            else:
                return "密码错误！"
        else:
            return "用户名不存在！"

    def verify_user_id(self, user_id):
        """
        Args:
            user_id

        Return:
            if user_id is exist, return True
            else return False
        """
        coll = self.db.user
        result = coll.find_one({"_id":ObjectId(user_id)})
        if result:
            return True
        else:
            return False

    def create_user(self, email, password):
        """
        Args:
            email
            password

        Return:
            If add successed, return the id of user, the type of id is bson.objectid.ObjectId.
            Else if failed, return the fail reason
        """
        if email != None and password != None:
            coll = self.db.user
            if coll.find_one({"email":email}):
                return "用户名已存在！"
            else:
                new_user = {"email":email, "password":self.__md5(password), "info":{}, "record":{}}
                return coll.insert_one(new_user).inserted_id
        else:
            return "输入有问题！"

    def get_user_info(self, user_id):
        """
        Args:
            user_id

        Return:
            return an object of user info
        """
        coll = self.db.user
        user_info = coll.find_one({"_id":ObjectId(user_id)})["info"]
        for attr in self.attr_list:
            if attr not in user_info.keys():
                user_info[attr] = ""
        return user_info

    def update_user_info(self, user_id, user_info):
        """
        Args:
            user_id
            user_info: a dict content user's info

        Return:
            return a string discribe if successed
        """
        coll = self.db.user
        result = coll.update_one({"_id":ObjectId(user_id)}, {'$set': {'info': user_info}})
        if result.matched_count > 0:
            return "保存成功"
        else:
            return "保存失败"

    def get_user_record(self, user_id, year, month):
        """
        Args:
            user_id
            year:
            month:

        Return:
            return an json content the result
        """
        coll = self.db.user
        key = "record."+year+"."+month
        result =  coll.find_one({"_id": ObjectId(user_id), key: { '$exists': True } })
        if result is not None:
            result = result["record"][year][month]
        return json.dumps(result)

    def update_user_record(self, user_id, record_key, record_value, date):
        """
        Args:
            user_id
            record_key : the key of value you want to update
            record_value : the value you want to update
            date : the record date, the format is {"year":xxxx, "month":xx, "day":xx}

        Return:
            return a string discribe if successed
        """
        coll = self.db.user
        if len(date["day"]) < 2:
            date["day"] = "0" + date["day"];
        key = 'record.{year}.{month}.{day}.{record_key}'.format(
            year=date["year"],
            month=date["month"],
            day=date["day"],
            record_key=record_key)
        result = coll.update_one(
            {'_id':ObjectId(user_id)},
            {
                '$set':
                {
                    key:record_value
                } 
            },
            True)
        if result.modified_count > 0:
            return "修改成功"
        else:
            return "无需修改"

    def get_order_people_info(self, user_id):
        """
        Args:
            user_id

        Return:
            return a list that contant the all order-people info
        """
        coll = self.db.user
        result = coll.find_one({ "_id": ObjectId(user_id), "order_people_info": { '$exists': True } })
        if result is not None:
            to_return = []
            for item in result["order_people_info"]:
                new_item = {'name': item['name'], 'value': json.dumps(item)}
                to_return.append(new_item)
            return to_return
        else:
            return []

    def update_order_people_info(self, user_id, name, id_card, telephone, hospital_card):
        """
        Args:
            user_id
            name
            id_card
            telephone
            hospital_card

        Return:
            return a list contant the insert info.
        """
        coll = self.db.user
        result = coll.find_one
        result = coll.update_one(
            {'_id': ObjectId(user_id)},
            {'$push':
                {
                    'order_people_info' : {
                        'name': name,
                        'id_card': id_card,
                        'telephone': telephone,
                        'hospital_card': hospital_card
                    }
                }
            },
            True)
        if result.modified_count > 0:
            return {'code': 200, 'info': '添加成功'}
        else:
            return {'code': 500, 'info': '添加失败'}



if __name__ == '__main__':
    user = User()
    print user.update_order_people_info("55f261d2f965b517181b33a9", "廖卢神", "362301199505241019", "15626470758", "123456")