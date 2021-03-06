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
  ''' 显示药品查询的结果 '''
  def post(self):
    #如果输入的为空字符串,则返回主页
    name_query_list = self.get_argument('name_query', None).split(' ')
    name_query = "".join(name_query_list)
    if name_query == '':
      self.redirect('/')
    name_query_list = list(name_query)

    func_query = self.get_argument('func_query', None)
    coll = self.application.db.medicine
    result_list = []   #用于存储符合所有查询条件的药品
    drug_list = []    #用于存储符合药品功能相符的药品
    
    if func_query.encode("utf-8") == "全部药品":
      drug_list = coll.find()
    else:
      drug_list = coll.find({"Function":func_query})

    for drug_item in drug_list:
      is_fit = True
      for name_query in name_query_list:
        if name_query not in drug_item["DrugName"]:
          is_fit = False
      if is_fit:
        result_list.append({"DrugName":drug_item["DrugName"],"storeCount":len(drug_item["DrugStore"])})

    self.render("search_result.html", name_query=self.get_argument('name_query'), func_query=func_query,
                                      community = self.get_argument("community"), result=result_list,
                                      is_index=False)

class DetailHandler(tornado.web.RequestHandler):
  """ 显示药品查询的详情 """
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
