#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from bson.objectid import ObjectId

from User import User
from img_create import create

from PIL import Image
import cStringIO as StringIO

from tornado.options import define, options
define("port", default=8100, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict (
            handlers=[(r'/', IndexHandler),
                            (r'/login', LoginHandler),
                            (r'/register', RegisterHandler),
                            (r'/userinfo', UserInfoHandler),
                            (r'/userrecord', UserRecordHandler),
                            (r'/userimg', ImageHandler)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login",
            debug=True
        )
        tornado.web.Application.__init__(self, **settings)

class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user_id")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html', warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user = User()
        result = user.verify_user(email, password)
        if isinstance(result, ObjectId):
            self.set_secure_cookie("user_id", str(result))
            self.redirect("/")
        else:
            self.render('login.html', warning=result)

class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html', warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        firmpassword = self.get_argument("firmpassword", None)
        if password != firmpassword:
            self.render('register.html', warning="两次密码输入不同！")
        else:
            user = User()
            result = user.create_user(email, password)
            if isinstance(result, ObjectId):
                self.set_secure_cookie("user_id", str(result))
                self.redirect("/")
            else:
                self.render('register.html', warning=result)

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = User()
        user_id = self.current_user
        self.render('user_info.html', user_info=user.get_user_info(user_id))

    def post(self):
        user_info = {}
        arg_list = ["name", "sex", "birth_date", "birth_locate",
        "job", "education", "blood", "RH", "marry", "history"]
        for arg in arg_list:
            user_info[arg] = self.get_argument(arg, "")
        user = User()
        user_id = self.current_user
        result = user.update_user_info(user_id, user_info)
        self.write(result)

class UserRecordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('clndr.html')

    def post(self):
        user_id = self.current_user
        user = User()
        if self.get_argument("info") == "get_user_record":
            year = self.get_argument("year")
            month =self.get_argument("month")
            self.write("year = " + year + " and month = " + month)
            # user.get_user_record(user_id, year, month)
        if self.get_argument("info") == "update_user_record":
            weight = self.get_argument("weight")
            self.write("your weight is " + weight + "kg")
            # user.update_user_record(user_id, xxxx)

class ImageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = User()
        user_info = user.get_user_info(self.current_user)
        fimg = create(user_info)
        fobj = StringIO.StringIO()
        fimg.save(fobj, format="png")
        for line in fobj.getvalue():
            self.write(line)
        self.set_header("Content-type",  "image/png")
        
        

if __name__ == '__main__':
    tornado.options.parse_command_line()
    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
