import socket
from _thread import *
import json

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = {}


def threaded_client(conn, player_id):
    conn.send(json.dumps({"player_id": player_id, "players": players}).encode())

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break

            data = json.loads(data)
            if data in ["UP", "DOWN", "LEFT", "RIGHT"]:
                if data == "UP":
                    players[player_id]["y"] -= 1
                elif data == "DOWN":
                    players[player_id]["y"] += 1
                elif data == "LEFT":
                    players[player_id]["x"] -= 1
                elif data == "RIGHT":
                    players[player_id]["x"] += 1

                conn.send(json.dumps({"players": players}).encode())

        except Exception as e:
            print(e)
            break

    print(f"[SERVER] Player {player_id} has disconnected.")
    del players[player_id]
    conn.close()


current_player_id = 0

while True:
    conn, addr = s.accept()
    print(f"[SERVER] Connected to: {addr}")

    players[current_player_id] = {"x": 50, "y": 50, "color": [255, 0, 0]}

    start_new_thread(threaded_client, (conn, current_player_id))
    current_player_id += 1
