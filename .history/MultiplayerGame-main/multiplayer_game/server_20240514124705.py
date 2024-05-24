import socket
from threading import Thread
import pickle
from game import Game

class Server:

    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.port = 4444
        self.server_settings = (self.server_ip, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game = Game()

    def start(self):
        try:
            self.server_socket.bind(self.server_settings)
        except Exception as e:
            print("[ERROR] Error trying to bind server.", e)

        self.server_socket.listen(10)
        self.listen_connections()
        print(f"[CONNECTION] Listening for connections on {self.port}")

    def listen_connections(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"[CONNECTION] Connection from {addr}")
            ACCEPT_THREAD = Thread(target=self.thread_client, args=(conn, addr))
            ACCEPT_THREAD.start()

    def thread_client(self, conn, addr):
        conn.send(pickle.dumps(self.game))
        is_online = True
        while is_online:
            try:
                data = pickle.loads(conn.recv(2048))
                self.game = data
                conn.sendall(pickle.dumps(self.game))
            except Exception as e:
                print(f"[SERVER] {addr} has disconnected.", e)
                is_online = False
        conn.close()

def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()
