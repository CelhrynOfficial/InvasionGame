import pygame
import sys
import pickle
from network import Network

WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invaders")

class GameClient:
    def __init__(self):
        self.window = window
        self.network = Network()
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        direction = ""
        if keys_pressed[pygame.K_UP]:
            direction = "UP"
        elif keys_pressed[pygame.K_DOWN]:
            direction = "DOWN"
        elif keys_pressed[pygame.K_LEFT]:
            direction = "LEFT"
        elif keys_pressed[pygame.K_RIGHT]:
            direction = "RIGHT"
        
        self.network.send(direction)

    def draw(self):
        self.window.fill((0, 255, 0))  # Fill the screen with black
        game_state = self.network.receive()
        if game_state:
            for player_id, player_data in game_state["players"].items():
                x = player_data["x"]
                y = player_data["y"]
                color = player_data["color"]
                pygame.draw.rect(self.window, color, pygame.Rect(x, y, 50, 50))

        pygame.display.update()

def main():
    game_client = GameClient()
    game_client.run()

if __name__ == "__main__":
    main()
