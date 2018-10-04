'''Responsive Design (Tornado Version)'''
# User Auth

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):

    def get(self):
        try:
            name = tornado.escape.xhtml_escape(self.current_user)
            if name == 'me':
                self.redirect('blog.html')
        except:
            self.render('index.html')

    def post(self):
        auth = {}
        auth['username'] = self.get_argument('username')
        auth['password'] = self.get_argument('password')
        try:
            auth['cookieuser'] = tornado.escape.xhtml_escape(self.current_user)
        except:
            auth['cookieuser'] = ''

        print 'AUTH (woohoo): ', auth

        if auth['username'] == 'me' and auth['password'] == 'woohoo':
            self.set_secure_cookie('user', self.get_argument('username'))
            self.render('blog.html')
        elif auth['cookieuser'] == 'me':
            self.render('blog.html')
        else:
            self.render('index.html')


class ClearHandler(tornado.web.RequestHandler):

    def get(self):
        self.clear_all_cookies()
        self.write('cookies cleared')


class BlogHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('blog.html')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
                  (r"/blog", BlogHandler),
                  (r"/clear", ClearHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret='abcdefg',
        # xsrf_cookies=True,
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
