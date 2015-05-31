#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo
from pymongo import MongoClient

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    settings = dict (
      handlers=[(r'/', SearchHandler), (r'/result', ResultHandler), (r'/detail', DetailHandler)],
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      debug=True
    )
    conn = MongoClient('localhost', 27017)
    self.db = conn["mydrug"]
    tornado.web.Application.__init__(self, **settings)

class SearchHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html', is_index=True)

class ResultHandler(tornado.web.RequestHandler):
  '''A RequestHandler to result'''
  def post(self):
    query = self.get_argument('query', None)
    result = []
    flag = True
    coll = self.application.db.medicine
    for doc in coll.find().sort("DrugName"):
      if query in doc["DrugName"]:
        name = doc["DrugName"]
        storeCount = len(doc["DrugStore"])
        result.append({"DrugName":name,"storeCount":storeCount})
    self.render("search_result.html", query=query, result=result, is_index=False)

class DetailHandler(tornado.web.RequestHandler):
  """docstring for DetailHandler"""
  def get(self):
    coll = self.application.db.medicine
    name = self.get_argument('name', None)
    detail = coll.find_one({"DrugName":name})
    self.render("search_detail.html", detail=detail, is_index=False)
    

if __name__ == '__main__':
  tornado.options.parse_command_line()
  HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
  HTTP_SERVER.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
