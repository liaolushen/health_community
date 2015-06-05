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
      handlers=[(r'/', SearchHandler), (r'/result', ResultHandler), (r'/detail/(.*)/(.*)', DetailHandler)],
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
    name_query = self.get_argument('name_query', None)
    func_query = self.get_argument('func_query', None)
    result = []
    flag = True
    coll = self.application.db.medicine
    if func_query.encode("utf-8") == "全部药品":
      for doc in coll.find().sort("DrugName"):
        if name_query in doc["DrugName"]:
          name = doc["DrugName"]
          storeCount = len(doc["DrugStore"])
          result.append({"DrugName":name,"storeCount":storeCount})
    else:
      for doc in coll.find({"Function":func_query}).sort("DrugName"):
        if name_query in doc["DrugName"]:
          name = doc["DrugName"]
          storeCount = len(doc["DrugStore"])
          result.append({"DrugName":name,"storeCount":storeCount})
    self.render("search_result.html", name_query=name_query, func_query=func_query,
                                      community = self.get_argument("community"), result=result,
                                      is_index=False)

class DetailHandler(tornado.web.RequestHandler):
  """docstring for DetailHandler"""
  def get(self, *args):
    coll = self.application.db.medicine
    locate = args[0]
    drugname = args[1]
    detail = coll.find_one({"DrugName":drugname})
    self.render("search_detail.html", detail=detail, locate=locate, is_index=False)
    

if __name__ == '__main__':
  tornado.options.parse_command_line()
  HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
  HTTP_SERVER.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
