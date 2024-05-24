import pygame

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, 50, 50))
