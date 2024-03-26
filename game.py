"""Exemple d'affichage d'une fenêtre simple."""
import pygame
from pygame.locals import *
import sys
import time



#Création des classes
class Ship:
    def __init__(self,x,y):
        self.sprit=pygame.image.load("bob4.svg")
        self.x = x
        self.y = y
        self.bullet=0

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
    
    def shot(self):
        
        self.bullet=Bullet(self)
        self.bullet.draw()
        
        

class Bullet:

    def __init__(self, ship):
        self.sprite=pygame.image.load("player.png")
        self.x=ship.x
        self.y=ship.y
        

    def draw(self):
        """
            Affichage du vaisseau
        """
        screen.blit(self.sprite,(self.x,self.y))
        pygame.display.flip()

class App:
    def __init__(self):
        """
            Initialisation de la fenêtre et des éléments
        """
        

        #Afficher le vaisseau
        screen.blit(background, (0, 0))
        self.ship=Ship((infoObject.current_w/2)-20,(infoObject.current_h-(infoObject.current_w/20))-20)


    def update(self):

        events = pygame.event.get()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.ship.move(-1,0)
            if event.key == pygame.K_RIGHT:
                self.ship.move(1,0)
            if event.key == pygame.K_TAB:
                self.ship.shot()
                

    def draw(self):
        # On affiche le vaisseau
        screen.fill((255,255,255))
        self.ship.draw()
        self.ship.bullet.draw()
        self.ship.bullet.y-=5
        



# Initialise screen
pygame.init()
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w-20, infoObject.current_h-20))
pygame.display.set_caption('Invaders')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()    
    
appli=App()
appli.ship.shot()


while True:

    #time.sleep(5/10000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    

    appli.update()
    appli.draw()
    


    

