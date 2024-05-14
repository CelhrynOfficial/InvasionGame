import json
import socket


def game_server():
    positions = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12000))
    while True:
        message, address = server_socket.recvfrom(1024)
        print("update from {}".format(address))
        positions[address] = json.loads(message.decode("utf8"))
        for client in positions.keys():
            if client != address:
                server_socket.sendto(message, client)
        print("game positions: {}".format(positions))

game_server()