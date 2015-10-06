#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import hashlib
import json

class Doctor(object):
    """ docstring for Doctor """
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn["health_manage"]

    def create_doctor(self, doctor_name, community, username, password):
        """
        Args:
            doctor_name: doctor's name that people can see
            community: the community that doctor belong to
            username: the name that admin use to login
            password: the password that admin use to login

        Return:
            if add success, return the id of doctor, the type of id is bson.objectid.ObjectId.
            Else if failed, return the fail reason
        """
        if doctor_name != None and community != None and username != None and password != None:
            coll = self.db.doctor
            if coll.find_one({"username":username}):
                return "用户名已存在！"
            else:
                new_doctor = {
                                "username": username,
                                "password": Doctor.md5(password),
                                "doctor_name": doctor_name,
                                "community": community
                            }
                return coll.insert_one(new_doctor).inserted_id
        else:
            return "输入有问题！"

    def get_all_doctors(self):
        """
        Args:
            None

        Return:
            a list by community, for example:
            [{
                "community": xxx,
                "doctor": 
                [{
                    "doctor_id": xxx,
                    "doctor_name": xxx
                }]
            }]
        """
        coll = self.db.doctor
        result = []
        for query_item in coll.find():

            new_doctor = {
                            "doctor_id": query_item["_id"],
                            "doctor_name": query_item["doctor_name"]
                         }

            isfind = False
            for result_item in result:
                if (query_item["community"] == result_item["community"]):
                    result_item["doctor"].append(new_doctor)
                    isfind = True

            if not isfind:
                new_community = {
                                    "community": query_item["community"],
                                    "doctor": []
                                }
                new_community["doctor"].append(new_doctor)
                result.append(new_community)

        return result

    def get_ordersize_by_date(self, date, doctor_id):
        """
        Args:
            date: the formate is yyyy-mm-dd
            doctor_id

        Return:
            a json of order size, if the order_size is not init, return 20,
            for example: {"morning": xx, "afternoon": xx}
        """
        coll = self.db.doctor
        date = date.split('-')
        key = "order_info."+date[0]+"."+date[1]+"."+date[2]
        result =  coll.find_one({"_id": ObjectId(doctor_id), key: { '$exists': True } })
        if result is None:
            return {"morning": 20, "afternoon": 20}
        else:
            return result["order_info"][date[0]][date[1]][date[2]]

    def update_doctor_order_info(self, date, doctor_id):
        """
        Args:
            date: the formate is yyyy-mm-dd
            doctor_id:
            time: the formate is 
            order_size:
        """
        pass

    @staticmethod
    def md5(str):
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()

if __name__ == '__main__':
    doctor = Doctor();
    print doctor.get_ordersize_by_date("2015-10-10", "5612a1f5f965b54fd7767f56")
