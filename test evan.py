"""Exemple d'affichage d'une fenêtre simple."""
import pygame
from pygame.locals import *
import sys
import time


"""

Cette version du jeu culte "Space invaders" est un projet scolaire de l'année 2023-2024
Nous sommes une équipes de trois eleves de Terminal NSI
Si vous souhaiter travailler dessus, veillez ne pas effacer ce message et actualiser le temps de travaille

Temps de travail: 3H

"""



#Création des classes
class Ship:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("player.png")
        self.x = x
        self.y = y
        self.bullets = []  # Liste pour stocker les lasers

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        for bullet in self.bullets:  # Dessinez tous les lasers
            bullet.draw()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x > infoObject.current_w - 65:
            self.x = infoObject.current_w - 65
        if self.x < 0:
            self.x = 0

    def shot(self):
        bullet = Bullet(self)  # Créez un nouveau laser
        self.bullets.append(bullet)  # Ajoutez le laser à la liste
        

        

class Bullet:

    def __init__(self, ship): #J'initialise mon 'Bullet'
        self.sprite=pygame.image.load("bob4.svg") #Son sprite
        self.x=ship.x #Ses coordonées
        self.y=ship.y
        

    def draw(self):
        """
            Affichage du vaisseau
        """
        screen.blit(self.sprite,(self.x,self.y)) #Je place mon missile à sa position
            
        
class enemie:
    def __init__(self, x, y):
        self.sprite=pygame.image.load("bob4.svg")
        self.x=x
        self.y=y
    def draw(self):
        screen.blit(self.sprite,(self.x,self.y)) #Je place mon missile à sa position

class band:
    def __init__(self):
        self.band=[]
        for i in range(10):
            for j in range(1):
                enemies=enemie(i*10, j*10)
                self.band.append(enemie)
        print(self.band)

class App:
    def __init__(self, speed=1):
        screen.blit(background, (0, 0))
        self.ship = Ship((infoObject.current_w / 2) - 20, (infoObject.current_h - (infoObject.current_h / 10)) - 20)
        self.speed = speed
        self.pressed_keys = []  # Liste pour stocker les touches enfoncées
        self.time=0 #Variables me permettant de gere l'envoie des laser
        self.timer=0
        self.groupe=band()
        

    def update(self, key_events):
        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.pressed_keys:  # Ajoutez la touche à la liste si elle n'y est pas déjà
                    self.pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:  # Supprimez la touche de la liste si elle y est
                    self.pressed_keys.remove(event.key)

        # Déplacez le vaisseau
        if pygame.K_LEFT in self.pressed_keys:
            self.ship.move(-1 * self.speed, 0)
        if pygame.K_RIGHT in self.pressed_keys:
            self.ship.move(1 * self.speed, 0)

        
        if pygame.K_SPACE in self.pressed_keys:
            self.timer=time.time()
            if self.timer-self.time>=0.5: #Cette conditionelle empche de tirer le missile trop vite
                self.ship.shot()
                self.time=self.timer

        # Mettez à jour la position de tous les lasers
        for bullet in self.ship.bullets:
            bullet.y -= 3 * self.speed

        # Supprimez les lasers qui ont quitté l'écran
        self.ship.bullets = [bullet for bullet in self.ship.bullets if bullet.y > -bullet.sprite.get_height()]

    def draw(self):
        screen.fill((255, 255, 255))  # J'efface l'écran précédent
        self.ship.draw()  # Je draw le vaisseau à sa nouvelle position
        for enemie in self.groupe.band:
            enemie.draw()
        for bullet in self.ship.bullets:  # Dessinez tous les lasers
            bullet.draw()
        pygame.display.flip()  # J'affiche tous les sprites

        


pygame.init() #Je crée l'interface pygame
infoObject = pygame.display.Info() #Je récupere les infos de l'ecran pour adapter la taille de la fenetre
screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h-20))#Je crée la fenetre en fonction de la taille de l'écran
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre


background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 
background = background.convert()
#background.fill((250, 250, 250)) #Je nettoie l'écran   
    
appli=App(2) #Je définie mon application, avec une valeur de vitesse


key_events = []  # Liste pour stocker les événements clavier

while True:  # Boucle principale du jeu

    for event in pygame.event.get():  # Récupère tous les événements pygame
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Stockez les événements clavier
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            key_events.append(event)

    # Mettez à jour et dessinez le jeu
    appli.update(key_events)
    appli.draw()
    
    key_events.clear()  # Nettoyez la liste des événements clavier après les avoir traités