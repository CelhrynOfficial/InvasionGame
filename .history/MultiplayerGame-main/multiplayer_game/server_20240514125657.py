import socket
from threading import Thread
import pickle
import random
import time
from player import Player

players = {}

class Server:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.port = 4444
        self.server_settings = (self.server_ip, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_index = 0
        self.global_score = 0

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
            ACCEPT_THREAD = Thread(target=self.thread_client, args=(conn, addr, self.player_index))
            ACCEPT_THREAD.start()
            self.player_index += 1

    def thread_client(self, conn, addr, player_index):
        rand_x = random.randrange(1, 50)
        rand_y = random.randrange(1, 50)
        color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

        player = Player(rand_x, rand_y, color)
        players[player_index] = player
        conn.send(pickle.dumps(players[player_index]))
        print("[SERVER] Started thread with player index:", player_index)
        
        is_online = True
        while is_online:
            try:
                data = pickle.loads(conn.recv(2048))
                players[player_index] = data

                # Envoyer l'état du jeu à tous les joueurs
                self.send_game_state()

                time.sleep(0.1)  # Attendez un court instant pour éviter d'envoyer trop de mises à jour
                
            except Exception as e:
                print(f"[SERVER] {addr} has disconnected.", e)
                is_online = False

        print(f"[SERVER] Ended threaded tasks for client: {addr}")
        self.player_index -= 1
        del players[player_index]
        conn.close()

    def send_game_state(self):
        game_state = {"players": {}}
        for player_id, player_data in players.items():
            game_state["players"][player_id] = {"x": player_data.x, "y": player_data.y, "color": player_data.color}
        for player_id, player_data in players.items():
            conn = player_data.conn
            try:
                conn.send(pickle.dumps(game_state))
            except:
                del players[player_id]
                print("[SERVER] Player disconnected.")

def main():
    server = Server()
    server.start()
    server.global_score = 0

if __name__ == '__main__':
    main()
