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
                            (r'/userrecord/(.*)', UserRecordHandler),
                            (r'/userimg', ImageHandler),
                            (r'/doctor/(.*)', DoctorHandler)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login",
            debug=True
        )
        tornado.web.Application.__init__(self, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = User()
        user_id = self.get_secure_cookie("user_id")
        if user.verify_user_id(user_id):
            return user_id
        else:
            self.clear_cookie("user_id")
            return None

class LoginHandler(BaseHandler):
    def get(self):
        next_page = self.get_argument("next", "/")
        self.render('login.html', next=next_page, warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        next_page = self.get_argument("next", "/")
        user = User()
        result = user.verify_user(email, password)
        if isinstance(result, ObjectId):
            self.set_secure_cookie("user_id", str(result))
            self.redirect(next_page)
        else:
            self.render('login.html', next=next_page, warning=result)

class RegisterHandler(BaseHandler):
    def get(self):
        next_page = self.get_argument("next", "/")
        self.render('register.html', next=next_page, warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        next_page = self.get_argument("next", "/")
        firmpassword = self.get_argument("firmpassword", None)
        if password != firmpassword:
            self.render('register.html', warning="两次密码输入不同！")
        else:
            user = User()
            result = user.create_user(email, password)
            if isinstance(result, ObjectId):
                self.set_secure_cookie("user_id", str(result))
                self.redirect(next_page)
            else:
                self.render('register.html', next=next_page, warning=result)

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = User()
        user_id = self.current_user
        self.render('user-info.html', user_info = user.get_user_info(user_id))

    def post(self):
        user_info = {}
        user = User()
        for attr in user.attr_list:
            user_info[attr] = self.get_argument(attr, "")
        user = User()
        user_id = self.current_user
        result = user.update_user_info(user_id, user_info)
        self.write(result)

class UserRecordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args):
        if args[0] == 'weight':
            self.render('weight.html')
        elif args[0] == 'bloodpressure':
            self.render('bloodpressure.html')
        elif args[0] == 'bloodglucose':
            self.render('bloodglucose.html')
        elif args[0] == 'bloodlipid':
            self.render('bloodlipid.html')
        else:
            self.redirect('/')

    def post(self, *args):
        user_id = self.current_user
        user = User()
        if args[0] == "get_user_record":
            year = self.get_argument("year")
            month =self.get_argument("month")
            result = user.get_user_record(user_id, year, month)
            self.set_header("Content-Type", "application/json")
            self.write(result)
            return

        date={}
        date["year"] = self.get_argument("year")
        date["month"] = self.get_argument("month")
        date["day"] = self.get_argument("day")

        if args[0] == "update_weight":
            result = user.update_user_record(user_id, "weight", self.get_argument("weight"), date)
            self.write(result)

        if args[0] == "update_bloodpressure":
            result = user.update_user_record(user_id, "bloodpressure", self.get_argument("bloodpressure"), date)
            self.write(result)

        if args[0] == "update_bloodglucose":
            result = user.update_user_record(user_id, "bloodglucose", self.get_argument("bloodglucose"), date)
            self.write(result)

        if args[0] == "update_bloodlipid":
            result = user.update_user_record(user_id, "bloodlipid", self.get_argument("bloodlipid"), date)
            self.write(result)

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
        
class DoctorHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args):
        if args[0] == '':
            self.render('doctor/index.html')
        else:
            self.write('<h1>功能正在开发，请耐心等待</h1>')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
