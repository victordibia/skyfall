from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from threading import Thread
import time

retry_threshold = 5
socket_url = "127.0.0.1"
socket_port = 5006

clients = []


class SimpleChat(WebSocket):

    def handleMessage(self):
        for client in clients:
            client.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        for client in clients:
            client.sendMessage(' - connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.address, 'closed')
        for client in clients:
            client.sendMessage(self.address[0] + u' - disconnected')


def sendMessage():
    print("sending message to ", len(clients), " clients")
    for client in clients:
        client.sendMessage("bingo")


def init():
    print("Starting websocket server")
    server = SimpleWebSocketServer('', socket_port, SimpleChat)
    server.serveforever()

    

thread = Thread(target=init)
thread.start()
# thread.join()

time.sleep(4)
print("number of clients", len(clients))
sendMessage()
