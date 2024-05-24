import random

class Game:
    def __init__(self):
        self.players = {}
        self.initialize_players()

    def initialize_players(self):
        for i in range(4):  # Initialize players
            rand_x = random.randrange(1, 50)
            rand_y = random.randrange(1, 50)
            color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            self.players[i] = {"x": rand_x, "y": rand_y, "color": color}

    def update_player_position(self, player_id, direction):
        player = self.players[player_id]
        if direction == "UP":
            player["y"] -= 1
        elif direction == "DOWN":
            player["y"] += 1
        elif direction == "LEFT":
            player["x"] -= 1
        elif direction == "RIGHT":
            player["x"] += 1
