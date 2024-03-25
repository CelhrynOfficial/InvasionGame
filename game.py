"""Exemple d'affichage d'une fenêtre simple."""
import pygame
from pygame.locals import *
import sys



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

class App:
    def __init__(self):
        """
            Initialisation de la fenêtre et des éléments
        """
        # Initialise screen
        pygame.init()
        infoObject = pygame.display.Info()
        screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        pygame.display.set_caption('Invaders')

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))


        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #Afficher le vaisseau
        screen.blit(background, (0, 0))
        ship=Ship(infoObject.current_w/2,infoObject.current_h-(infoObject.current_w/20))
        ship.draw()









while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    App()
    

    