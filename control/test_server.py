# https://github.com/Pithikos/python-websocket-server
import logging
from websocket_server import WebsocketServer

def new_client(client, server):
    print('connected!')
    server.send_message_to_all("Hey all, a new client has joined us")

def message_received(client, server, message):
    ##Put my logic here
    print(message + "\r\n")


server = WebsocketServer(5005, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()