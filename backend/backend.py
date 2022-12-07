# -*- coding: utf-8 -*-
 
import os
 
import tornado.httpserver
import pika
import tornado.ioloop
import tornado.options
import tornado.web
import json
 
from tornado.options import define, options





 
define("port", default=8888, help="run on the given port", type=int)
 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)
 

 
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print('Got JSON data:', data)
        self.write({ 'got' : 'your data' })
        
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='', routing_key='hello', body=(str(data["surname"]))+"_"+str(data["name"])+"_"+str(data["patronymic"])+"_"+str(data["phone"])+"_"+str(data["appeal"]))
        connection.close()


    def options(self, *args):
        self.set_status(204)
        self.finish()
 
class RootHandler(BaseHandler):
    def get(self):
        result = list(self.db.contents.find({}, limit=1))[0]["_id"]
        self.write(str(result))
 
 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
 
if __name__ == "__main__":
    main()
   


    