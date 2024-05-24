import socket
import pickle

class Network:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = 4445
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.socket_client.connect((self.server_ip, self.server_port))
            self.game_state = pickle.loads(self.socket_client.recv(2048))
        except Exception as e:
            print("[ERROR] Error trying to connect to server", e)

    def send(self, data):
        try:
            self.socket_client.send(pickle.dumps(data))
        except Exception as e:
            print("[ERROR] Error trying to send data to server.", e)

    def receive(self):
        try:
            self.game_state = pickle.loads(self.socket_client.recv(2048))
            return self.game_state
        except Exception as e:
            print("[ERROR] Error trying to receive data from server.", e)
