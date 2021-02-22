# import websockets
# import logging
# from websockets import WebSocketServerProtocol
# import asyncio
# #--------------------------------------------------------------------------------------------------------
# logging.basicConfig(level = logging.INFO)

# class Server:
#     clients = set()

#     async def register(self, ws: WebSocketServerProtocol) -> None:
#         self.clients.add(ws)
#         logging.info(f'{ws.remote_address} connects.')

#     async def unregister(self, ws: WebSocketServerProtocol) -> None:
#         self.clients.remove(ws)
#         logging.info(f'{ws.remote_address} disconnects.')

#     async def send_to_clients(self, message: str) -> None:
#         if self.clients:
#             await asyncio.wait([client.send(message) for client in self.clients])

#     async def distribute(self, ws: WebSocketServerProtocol) -> None:
#         async for message in ws:
#             await self.send_to_clients(message)


#     async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
#         await self.register(ws)
# #        try:
#         await self.distribute(ws)
# #        catch: 
#  #           print("hola")
#  #       finally:
#  #           await self.unregister(ws)
        

# server = Server()
# start_server = websockets.serve(server.ws_handler, 'localhost' , 4000 )
# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_server)
# loop.run_forever()



# from websocket_server import WebsocketServer

# # Called for every client connecting (after handshake)
# def new_client(client, server):
# 	print("New client connected and was given id %d" % client['id'])
# 	server.send_message_to_all("Hey all, a new client has joined us")


# # Called for every client disconnecting
# def client_left(client, server):
# 	print("Client(%d) disconnected" % client['id'])


# # Called when a client sends a message
# def message_received(client, server, message):
# 	if len(message) > 200:
# 		message = message[:200]+'..'
# 	print("Client(%d) said: %s" % (client['id'], message))


# PORT=9001
# server = WebsocketServer(PORT)
# server.set_fn_new_client(new_client)
# server.set_fn_client_left(client_left)
# server.set_fn_message_received(message_received)
# server.run_forever()


# import tornado.httpserver
# import tornado.websocket
# import tornado.ioloop
# import tornado.web
# import socket
# '''
# This is a simple Websocket Echo server that uses the Tornado websocket handler.
# Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
# This program will echo back the reverse of whatever it recieves.
# Messages are output to the terminal for debuggin purposes. 
# ''' 
 
# class WSHandler(tornado.websocket.WebSocketHandler):
#     def open(self):
#         print ("new connection")
      
#     def on_message(self, message):
#         print ("message received:  %s" % message)
#         # Reverse Message and send it back
#         print ("sending back message: %s" % message[::-1])
#         self.write_message(message[::-1])
 
#     def on_close(self):
#         print ("connection closed")
 
#     def check_origin(self, origin):
#         return True
 
# application = tornado.web.Application([
#     (r'/ws', WSHandler),
# ])
 
 
# if __name__ == "__main__":
#     http_server = tornado.httpserver.HTTPServer(application)
#     http_server.listen(8888)
#     myIP = socket.gethostbyname(socket.gethostname())
#     print ("*** Websocket Server Started at %s***" % myIP)
#     tornado.ioloop.IOLoop.instance().start()

import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import qwiic_titan_gps
import json

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")
        self.callback = tornado.ioloop.PeriodicCallback(self.send_signal, 5000)
        self.callback.start()
        
    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))
        print ("message received:  %s" % message)
#        Reverse Message and send it back
        print ("sending back message: %s" % message[::-1])
        self.write_message(message[::-1])
    
    def send_signal(self, qwiicGPS):
        data = {"Latitude":qwiicGPS.gnss_messages['Latitude'] , "Longitude":qwiicGPS.gnss_messages['Longitude'] , "Altitude":qwiicGPS.gnss_messages['Altitude'], "Time":qwiicGPS.gnss_messages['Time'], "Sat_Number":qwiicGPS.gnss_messages['Sat_Number']}
        self.write_message(json.dumps(data))
    



def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    qwiicGPS = qwiic_titan_gps.QwiicTitanGps()
    qwiicGPS.begin()
    
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()



    



