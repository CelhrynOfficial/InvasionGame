"""Exemple d'affichage d'une fenêtre simple."""
import pygame
from pygame.locals import *
import sys
from settings import Settings 
ai_settings = Settings()

#Création des classes
class Ship:
    def __init__(self,x,y):
        self.sprit=pygame.image.load("player.png")
        self.x = x
        self.y = y

    def draw(self):
        """
            Affichage du vaisseau
        """
        screen.blit(self.sprit,(self.x,self.y))
        pygame.display.flip()       

    def move(self, dx, dy):
        """
            Déplacement du vaisseau
        """
        self.x += dx
        self.y += dy




# Initialise screen
pygame.init()
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption('Invaders')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.blit(background, (0, 0))
    ship=Ship(0,0)
    ship.draw()
    

    