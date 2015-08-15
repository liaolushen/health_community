#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from user import User

from tornado.options import define, options
define("port", default=8100, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict (
            handlers=[(r'/', IndexHandler),
                            (r'/login', LoginHandler),
                            (r'/register', RegisterHandler)],
            # handlers=[(r'/', IndexHandler),
            #                   (r'/login', LoginHandler),
            #                   (r'/detail/(.*)/(.*)', DetailHandler)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login",
            debug=True
        )
        tornado.web.Application.__init__(self, **settings)

class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("email")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html', warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user = User()
        result = user.verifyUser(email, password)
        if result is None:
            self.set_secure_cookie("email", self.get_argument("email"))
            self.redirect("/")
        else:
            self.render('login.html', warning=result)

class RegisterHandler(BaseHandler):
    def  get(self):
        self.render('register.html', warning=None)
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        firmpassword = self.get_argument("firmpassword", None)
        if password != firmpassword:
            self.render('register.html', warning="两次密码输入不同！")
        else:
            user = User()
            result = user.addUser(email, password)
            if result is None:
                self.set_secure_cookie("email", self.get_argument("email"))
                self.redirect("/")
            else:
                self.render('register.html', warning=result)
        
        

if __name__ == '__main__':
    tornado.options.parse_command_line()
    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
