## Author: Victor Dibia
## Web socket client which is used to send socket messages to a connected server.


import websocket
import time
import json
from websocket import WebSocketException, WebSocketConnectionClosedException
import sys
#import _thread as thread

import websocket
ws = websocket.WebSocket()
retry_threshold = 5
socketurl = ""


def send_message(message, source):
    global ws

    payload = json.dumps(
        {'event': 'detect', 'data': message, "source": source})
    # print("sending message")
    try:
        ws.send(payload)
    except WebSocketException:
        print(
            "Error: something went wrong with the socket. Retrying after ", retry_threshold)
        reconnect_socket()
    except WebSocketConnectionClosedException:
        print("Error: Connection is closed. Retrying after ", retry_threshold)
        reconnect_socket()
    except BrokenPipeError:
        print("Error: Broken Pipe. Retrying after ", retry_threshold)
        reconnect_socket()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise




def reconnect_socket():
    time.sleep(retry_threshold)
    print("Reconnecting websocket ......", socketurl)
    socket_init(socketurl) 


ws = None


def socket_init(url):
    global ws, socketurl
    socketurl = url
    ws = websocket.WebSocket()
    try:
        ws.connect(url)
        print("Websocket connection successful")
    except ConnectionRefusedError:
        print("Websocket Connection refused")
        reconnect_socket()

 
