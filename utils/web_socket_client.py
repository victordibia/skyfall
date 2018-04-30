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
            "Error: somthing went wrong with the socket. Retrying after ", retry_threshold)
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


def print_values(classes, scores, boxes, category_index, min_score_thresh):

    tags = []
    for i in range(boxes.shape[0]):
        if scores[i] > min_score_thresh:
            if category_index[classes[i]]['name'] == "hand" and boxes[i][3] - boxes[i][1] > 0.3:
                break
            if classes[i] in category_index.keys():
                class_name = category_index[classes[i]]['name']
            else:
                class_name = 'N/A'
            display_str = '{}: {}%'.format(
                class_name,
                int(100 * scores[i]))
            tag = {}
            tag['class'] = class_name
            tag['score'] = scores[i].tolist()
            tag['box'] = boxes[i].tolist()
            tags.append(tag)
    if (len(tags) > 0):
        send_message(tags)
        print(tags)


def reconnect_socket():
    time.sleep(retry_threshold)
    print("Reconnecting websocket ......", socketurl)
    socket_init(socketurl)

    # def run(*args):
    #     time.sleep(retry_threshold)
    #     socket_init(socketurl)
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())


ws = None


def socket_init(url):
    global ws, socketurl
    socketurl = url
    ws = websocket.WebSocket()
    try:
        ws.connect(url)
        print("Websocket connection successful")
    except ConnectionRefusedError:
        print("Connection refused")
        reconnect_socket()

#
# socket_init("ws://localhost:8068")
# tag = {}
# tag['class'] = "class_name"
# tag['score'] = [1, 2]
# send_message(tag)
