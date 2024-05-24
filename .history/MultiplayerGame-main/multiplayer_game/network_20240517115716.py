import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = json.loads(self.client.recv(2048).decode())
            self.player_id = data["player_id"]
            return self.player_id
        except:
            pass

    def send(self, data):
        try:
            self.client.send(data.encode())
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return json.loads(self.client.recv(2048).decode())
        except socket.error as e:
            print(e)
