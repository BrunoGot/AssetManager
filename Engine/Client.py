import socket
from struct import pack
"""the asset manager should act as a server in the dcc communication. That allowing multiple connection with the same kind of DCCs
this file should be renamed as 'server'
"""


class Server():
    def __init__(self):
        self.max_client = 5
        pass

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 80))
        self.socket.listen(self.max_client)

    def listen(self):
        print("start listening")
        (clientsock, adress) = self.socket.accept()
        client = ClientHandler(clientsock, adress)
        client.start()
        print("client created")


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('localhost', 80))
#print("connected")

while True:
    sent = socket.send('t'.encode())

